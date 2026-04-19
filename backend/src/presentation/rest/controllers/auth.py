from typing import Annotated
from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Query, Response, status
from module.auth.application import AuthService, parse_auth_provider
from module.auth.infra.oidc import (
    AuthenticatedUser,
    AuthProvider,
    InvalidCredentials,
    VerifiedIdentity,
    ZitadelOidcClient,
)

from presentation.rest.dto import (
    AuthIdentityResponse,
    AuthorizationUrlResponse,
    CurrentUserResponse,
    LinkIdentityRequest,
    OidcAuthPayloadRequest,
    TelegramAuthPayload,
    TokenExchangeRequest,
    TokenResponse,
)

auth_router = APIRouter(route_class=DishkaRoute)


@auth_router.get(
    "/login-url",
    summary="Build Zitadel authorization URL",
)
async def login_url(
    client: FromDishka[ZitadelOidcClient],
    state: Annotated[str | None, Query()] = None,
    nonce: Annotated[str | None, Query()] = None,
) -> AuthorizationUrlResponse:
    return AuthorizationUrlResponse(url=client.authorization_url(state=state, nonce=nonce))


@auth_router.post(
    "/callback",
    summary="Exchange Zitadel authorization code for tokens",
)
async def exchange_code(
    payload: TokenExchangeRequest,
    client: FromDishka[ZitadelOidcClient],
) -> TokenResponse:
    token_payload = await client.exchange_code(payload.code, code_verifier=payload.code_verifier)

    return TokenResponse.model_validate(token_payload)


@auth_router.post(
    "/telegram",
    summary="Authenticate with Telegram login payload",
)
async def authenticate_telegram(
    payload: TelegramAuthPayload,
    auth_service: FromDishka[AuthService],
) -> CurrentUserResponse:
    current_user = await auth_service.authenticate_telegram(payload.model_dump(exclude_none=True))

    return CurrentUserResponse.model_validate(current_user, from_attributes=True)


@auth_router.post(
    "/oidc/callback",
    summary="Authenticate with verified OIDC access token",
)
async def authenticate_oidc(
    payload: OidcAuthPayloadRequest,
    auth_service: FromDishka[AuthService],
) -> CurrentUserResponse:
    provider = parse_auth_provider(payload.provider)
    current_user = await auth_service.authenticate_oidc(payload.access_token, provider)

    return CurrentUserResponse.model_validate(current_user, from_attributes=True)


@auth_router.get(
    "/me",
    summary="Return current authenticated user",
)
async def me(
    current_user: FromDishka[AuthenticatedUser],
) -> CurrentUserResponse:
    return CurrentUserResponse.model_validate(current_user, from_attributes=True)


@auth_router.get(
    "/identities",
    summary="List current user login methods",
)
async def list_identities(
    current_user: FromDishka[AuthenticatedUser],
    auth_service: FromDishka[AuthService],
) -> list[AuthIdentityResponse]:
    identities = await auth_service.list_identities(current_user.user_id)
    return [
        AuthIdentityResponse(
            id=identity.id,
            provider=identity.provider.value,
            username=identity.username,
            email=identity.email,
        )
        for identity in identities
    ]


@auth_router.post(
    "/identities/link",
    summary="Link a new login method to current user",
)
async def link_identity(
    payload: LinkIdentityRequest,
    current_user: FromDishka[AuthenticatedUser],
    auth_service: FromDishka[AuthService],
) -> AuthIdentityResponse:
    verified_identity = await _verify_link_payload(payload, auth_service)
    identity = await auth_service.link_identity(current_user.user_id, verified_identity)

    return AuthIdentityResponse(
        id=identity.id,
        provider=identity.provider.value,
        username=identity.username,
        email=identity.email,
    )


@auth_router.delete(
    "/identities/{identity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Unlink current user login method",
)
async def unlink_identity(
    identity_id: UUID,
    current_user: FromDishka[AuthenticatedUser],
    auth_service: FromDishka[AuthService],
) -> Response:
    await auth_service.unlink_identity(current_user.user_id, identity_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def _verify_link_payload(payload: LinkIdentityRequest, auth_service: AuthService) -> VerifiedIdentity:
    provider = parse_auth_provider(payload.provider)
    if provider == AuthProvider.TELEGRAM:
        if payload.telegram_payload is None:
            msg = "Missing Telegram auth payload"
            raise InvalidCredentials(msg)
        return auth_service.verify_telegram_identity(payload.telegram_payload.model_dump(exclude_none=True))

    if payload.access_token is None:
        msg = "Missing OIDC access token"
        raise InvalidCredentials(msg)
    return await auth_service.verify_oidc_identity(payload.access_token, provider)
