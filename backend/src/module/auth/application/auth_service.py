from uuid import UUID

from module.auth.infra.db import AuthRepository
from module.auth.infra.oidc import (
    AuthenticatedUser,
    AuthIdentity,
    AuthProvider,
    InvalidCredentials,
    OidcTokenVerifier,
    TelegramAuthVerifier,
    UnsupportedProvider,
    UserForbidden,
    UserStatus,
    VerifiedIdentity,
)


class AuthService:
    def __init__(
        self,
        repository: AuthRepository,
        telegram_verifier: TelegramAuthVerifier,
        oidc_verifier: OidcTokenVerifier,
    ) -> None:
        self._repository = repository
        self._telegram_verifier = telegram_verifier
        self._oidc_verifier = oidc_verifier

    async def authenticate_telegram(self, payload: dict) -> AuthenticatedUser:
        identity = self._telegram_verifier.verify(payload)
        return await self._login_or_create(identity)

    async def authenticate_oidc(self, token: str, provider: AuthProvider) -> AuthenticatedUser:
        identity = await self._oidc_verifier.verify(token, provider)
        return await self._login_or_create(identity)

    async def verify_oidc_identity(self, token: str, provider: AuthProvider) -> VerifiedIdentity:
        return await self._oidc_verifier.verify(token, provider)

    def verify_telegram_identity(self, payload: dict) -> VerifiedIdentity:
        return self._telegram_verifier.verify(payload)

    async def get_current_user(self, token: str, provider: AuthProvider = AuthProvider.ZITADEL) -> AuthenticatedUser:
        return await self.authenticate_oidc(token, provider)

    async def link_identity(self, current_user_id: UUID, identity: VerifiedIdentity) -> AuthIdentity:
        user = await self._repository.get_user(current_user_id)
        if user is None:
            msg = "Current user not found"
            raise InvalidCredentials(msg)
        self._ensure_user_allowed(user.status)
        return await self._repository.link_identity(current_user_id, identity)

    async def list_identities(self, user_id: UUID) -> list[AuthIdentity]:
        return await self._repository.list_identities(user_id)

    async def unlink_identity(self, user_id: UUID, identity_id: UUID) -> None:
        await self._repository.unlink_identity(user_id, identity_id)

    async def _login_or_create(self, identity: VerifiedIdentity) -> AuthenticatedUser:
        user, auth_identity = await self._repository.login_or_create_user(identity)
        self._ensure_user_allowed(user.status)
        return AuthenticatedUser(
            user_id=user.id,
            identity_id=auth_identity.id,
            provider=auth_identity.provider.value,
            subject=auth_identity.subject,
            status=user.status.value,
        )

    @staticmethod
    def _ensure_user_allowed(status: UserStatus) -> None:
        if status in {UserStatus.SUSPENDED, UserStatus.BANNED}:
            msg = "User is suspended or banned"
            raise UserForbidden(msg)

    # async def provide_current_user(
    #     self,
    #     request: Request,
    # ) -> AuthenticatedUser:
    #     token = self._extract_bearer_token(request)
    #     provider = parse_auth_provider(
    #         request.query_params.get("provider", AuthProviderEnum.ZITADEL.value),
    #     )
    #     auth_service = await request.state.dishka_container.get(AuthService)
    #
    #     try:
    #         return await auth_service.get_current_user(token, provider)
    #     except InvalidCredentials as exc:
    #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    #     except AuthError as exc:
    #         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)) from exc
    #
    # @staticmethod
    # def _extract_bearer_token(request: Request) -> str:
    #     authorization = request.headers.get("Authorization")
    #     if authorization is None:
    #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")
    #
    #     scheme, _, token = authorization.partition(" ")
    #     if scheme.lower() != "bearer" or not token:
    #         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    #
    #     return token


def parse_auth_provider(value: str) -> AuthProvider:
    try:
        return AuthProvider(value)
    except ValueError as exc:
        msg = "Unsupported auth provider"
        raise UnsupportedProvider(msg) from exc
