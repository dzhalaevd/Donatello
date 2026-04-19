from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuthorizationUrlResponse(BaseModel):
    url: str


class TokenExchangeRequest(BaseModel):
    code: str
    code_verifier: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int | None = None
    refresh_token: str | None = None
    id_token: str | None = None
    scope: str | None = None

    model_config = ConfigDict(extra="allow")


class TelegramAuthPayload(BaseModel):
    id: int
    auth_date: int
    hash: str
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    photo_url: str | None = None


class OidcAuthPayloadRequest(BaseModel):
    access_token: str
    provider: str = "zitadel"


class LinkIdentityRequest(BaseModel):
    provider: str
    access_token: str | None = None
    telegram_payload: TelegramAuthPayload | None = None


class CurrentUserResponse(BaseModel):
    user_id: UUID
    identity_id: UUID
    provider: str
    subject: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class AuthIdentityResponse(BaseModel):
    id: UUID
    provider: str
    username: str | None
    email: str | None
