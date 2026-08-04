from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    telegram_bot_token: str | None = Field(default=None, alias="TELEGRAM_BOT_TOKEN")
    telegram_auth_ttl_seconds: int = Field(default=86400, alias="TELEGRAM_AUTH_TTL_SECONDS")

    issuer: AnyHttpUrl = Field(default=AnyHttpUrl("http://localhost:8080"), alias="ZITADEL_ISSUER")
    client_id: str | None = Field(default=None, alias="ZITADEL_CLIENT_ID")
    client_secret: str | None = Field(default=None, alias="ZITADEL_CLIENT_SECRET")
    redirect_uri: AnyHttpUrl = Field(
        default=AnyHttpUrl("http://localhost:8000/api/v1/auth/callback"),
        alias="ZITADEL_REDIRECT_URI",
    )
    audience: str | None = Field(default=None, alias="ZITADEL_AUDIENCE")
    scopes: str = Field(default="openid profile email offline_access", alias="ZITADEL_SCOPES")
    jwks_cache_ttl_seconds: int = Field(default=300, alias="ZITADEL_JWKS_CACHE_TTL_SECONDS")
    http_timeout_seconds: float = Field(default=10.0, alias="ZITADEL_HTTP_TIMEOUT_SECONDS")
    casdoor_issuer: AnyHttpUrl | None = Field(default=None, alias="CASDOOR_ISSUER")
    casdoor_audience: str | None = Field(default=None, alias="CASDOOR_AUDIENCE")

    model_config = SettingsConfigDict(
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def issuer_url(self) -> str:
        return str(self.issuer).rstrip("/")

    @property
    def redirect_uri_url(self) -> str:
        return str(self.redirect_uri)
