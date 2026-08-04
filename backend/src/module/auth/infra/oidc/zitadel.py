import json
import time
from typing import Any, cast
from urllib.parse import urlencode

import httpx
import jwt
from jwt import InvalidTokenError
from jwt.algorithms import RSAAlgorithm

from module.auth.infra.config import AuthConfig

from .dto import AuthProvider, VerifiedIdentity
from .exceptions import (
    InvalidCredentials,
    UnsupportedProvider,
    ZitadelConfigurationError,
    ZitadelTokenError,
)


class ZitadelOidcClient:
    def __init__(self, settings: AuthConfig) -> None:
        self._settings = settings
        self._openid_configuration: dict[str, Any] | None = None
        self._jwks: dict[str, Any] | None = None
        self._jwks_loaded_at = 0.0

    def authorization_url(self, *, state: str | None = None, nonce: str | None = None) -> str:
        if not self._settings.client_id:
            msg = "Zitadel client id is not configured"
            raise ZitadelConfigurationError(msg)

        params = {
            "client_id": self._settings.client_id,
            "redirect_uri": self._settings.redirect_uri_url,
            "response_type": "code",
            "scope": self._settings.scopes,
        }
        if state:
            params["state"] = state
        if nonce:
            params["nonce"] = nonce

        return f"{self._settings.issuer_url}/oauth/v2/authorize?{urlencode(params)}"

    async def exchange_code(self, code: str, *, code_verifier: str | None = None) -> dict[str, Any]:
        if not self._settings.client_id:
            msg = "Zitadel client id is not configured"
            raise ZitadelConfigurationError(msg)

        config = await self._get_openid_configuration()
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self._settings.redirect_uri_url,
            "client_id": self._settings.client_id,
        }
        if code_verifier:
            data["code_verifier"] = code_verifier
        auth: tuple[str, str] | None = None
        if self._settings.client_secret:
            auth = (self._settings.client_id, self._settings.client_secret)

        async with httpx.AsyncClient(timeout=self._settings.http_timeout_seconds) as client:
            response = await client.post(config["token_endpoint"], data=data, auth=auth)

        if response.status_code >= 400:
            msg = "Zitadel rejected authorization code"
            raise ZitadelTokenError(msg)
        return cast("dict[str, Any]", response.json())

    async def get_userinfo(self, access_token: str) -> dict[str, Any]:
        config = await self._get_openid_configuration()
        async with httpx.AsyncClient(timeout=self._settings.http_timeout_seconds) as client:
            response = await client.get(
                config["userinfo_endpoint"],
                headers={"Authorization": f"Bearer {access_token}"},
            )

        if response.status_code >= 400:
            msg = "Zitadel rejected access token"
            raise ZitadelTokenError(msg)
        return cast("dict[str, Any]", response.json())

    async def verify_access_token(self, token: str) -> dict[str, Any]:
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        if not kid:
            msg = "Token header has no key id"
            raise ZitadelTokenError(msg)

        jwk = await self._get_jwk(kid)
        key = RSAAlgorithm.from_jwk(json.dumps(jwk))
        options = {"verify_aud": self._settings.audience is not None}

        try:
            return cast(
                "dict[str, Any]",
                jwt.decode(
                    token,
                    key=key,
                    algorithms=[jwk.get("alg", "RS256")],
                    audience=self._settings.audience,
                    issuer=self._settings.issuer_url,
                    options=options,
                ),
            )
        except InvalidTokenError as exc:
            msg = "Invalid Zitadel token"
            raise ZitadelTokenError(msg) from exc

    async def _get_openid_configuration(self) -> dict[str, Any]:
        if self._openid_configuration is not None:
            return self._openid_configuration

        url = f"{self._settings.issuer_url}/.well-known/openid-configuration"
        async with httpx.AsyncClient(timeout=self._settings.http_timeout_seconds) as client:
            response = await client.get(url)

        if response.status_code >= 400:
            msg = "Cannot load Zitadel OpenID configuration"
            raise ZitadelConfigurationError(msg)

        self._openid_configuration = cast("dict[str, Any]", response.json())
        return self._openid_configuration

    async def _get_jwk(self, kid: str) -> dict[str, Any]:
        jwks = await self._get_jwks()
        for jwk in cast("list[dict[str, Any]]", jwks.get("keys", [])):
            if jwk.get("kid") == kid:
                return jwk

        self._jwks = None
        jwks = await self._get_jwks()
        for jwk in cast("list[dict[str, Any]]", jwks.get("keys", [])):
            if jwk.get("kid") == kid:
                return jwk

        msg = "Token key is not present in Zitadel JWKS"
        raise ZitadelTokenError(msg)

    async def _get_jwks(self) -> dict[str, Any]:
        now = time.monotonic()
        if self._jwks is not None and now - self._jwks_loaded_at < self._settings.jwks_cache_ttl_seconds:
            return self._jwks

        config = await self._get_openid_configuration()
        async with httpx.AsyncClient(timeout=self._settings.http_timeout_seconds) as client:
            response = await client.get(config["jwks_uri"])

        if response.status_code >= 400:
            msg = "Cannot load Zitadel JWKS"
            raise ZitadelConfigurationError(msg)

        self._jwks = cast("dict[str, Any]", response.json())
        self._jwks_loaded_at = now
        return self._jwks


class OidcTokenVerifier:
    def __init__(self, zitadel_client: ZitadelOidcClient, settings: AuthConfig) -> None:
        self._zitadel_client = zitadel_client
        self._settings = settings

    async def verify(self, token: str, provider: AuthProvider) -> VerifiedIdentity:
        if provider == AuthProvider.ZITADEL:
            claims = await self._verify_zitadel(token)
        elif provider == AuthProvider.CASDOOR:
            claims = await self._verify_casdoor(token)
        else:
            msg = "Unsupported OIDC provider"
            raise UnsupportedProvider(msg)

        subject = claims.get("sub")
        if not subject:
            msg = "OIDC token has no subject"
            raise InvalidCredentials(msg)

        return VerifiedIdentity(
            provider=provider,
            subject=str(subject),
            email=claims.get("email"),
            username=claims.get("preferred_username") or claims.get("username") or claims.get("name"),
        )

    async def _verify_zitadel(self, token: str) -> dict[str, Any]:
        try:
            return await self._zitadel_client.verify_access_token(token)
        except ZitadelTokenError as exc:
            raise InvalidCredentials(str(exc)) from exc

    async def _verify_casdoor(self, token: str) -> dict[str, Any]:
        if not self._settings.casdoor_issuer:
            msg = "Casdoor auth is not configured"
            raise UnsupportedProvider(msg)

        issuer = str(self._settings.casdoor_issuer).rstrip("/")
        header = jwt.get_unverified_header(token)
        kid = header.get("kid")
        if not kid:
            msg = "OIDC token header has no key id"
            raise InvalidCredentials(msg)

        jwk = await self._get_casdoor_jwk(issuer, kid)
        return self._decode_casdoor_token(token, jwk, issuer)

    async def _get_casdoor_jwk(self, issuer: str, kid: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self._settings.http_timeout_seconds) as client:
            config_response = await client.get(f"{issuer}/.well-known/openid-configuration")
            if config_response.status_code >= 400:
                msg = "Cannot load Casdoor OpenID configuration"
                raise UnsupportedProvider(msg)
            jwks_response = await client.get(config_response.json()["jwks_uri"])
            if jwks_response.status_code >= 400:
                msg = "Cannot load Casdoor JWKS"
                raise UnsupportedProvider(msg)

        jwk = next((key for key in jwks_response.json().get("keys", []) if key.get("kid") == kid), None)
        if jwk is None:
            msg = "OIDC token key is not present in JWKS"
            raise InvalidCredentials(msg)
        return cast("dict[str, Any]", jwk)

    def _decode_casdoor_token(self, token: str, jwk: dict[str, Any], issuer: str) -> dict[str, Any]:
        try:
            key = RSAAlgorithm.from_jwk(json.dumps(jwk))
            return cast(
                "dict[str, Any]",
                jwt.decode(
                    token,
                    key=key,
                    algorithms=[jwk.get("alg", "RS256")],
                    options={"verify_aud": self._settings.casdoor_audience is not None},
                    audience=self._settings.casdoor_audience,
                    issuer=issuer,
                ),
            )
        except InvalidTokenError as exc:
            msg = "Invalid Casdoor token"
            raise InvalidCredentials(msg) from exc
