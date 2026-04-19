from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from environs import Env
from module.auth.application import AuthService
from module.auth.infra.config import AuthConfig
from module.auth.infra.db import AuthRepository
from module.auth.infra.oidc import (
    OidcTokenVerifier,
    TelegramAuthVerifier,
    ZitadelOidcClient,
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from infra.db import DbConfig, SQLAlchemyUoW, UnitOfWork


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_env(self) -> Env:
        env = Env()
        env.read_env()
        return env

    @provide(scope=Scope.APP)
    def provide_db_config(self, env: Env) -> DbConfig:
        return DbConfig.from_env(env)

    @provide(scope=Scope.APP)
    def provide_auth_config(self) -> AuthConfig:
        return AuthConfig()


class SqlalchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_engine(self, config: DbConfig) -> AsyncEngine:
        return create_async_engine(
            config.construct_sqlalchemy_url(),
            pool_size=10,
            max_overflow=5,
        )

    @provide(scope=Scope.APP)
    def provide_sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(self, sessionmaker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def provide_uow(self, session: AsyncSession) -> UnitOfWork:
        return SQLAlchemyUoW(session)


class AuthServicesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_auth_repository(self, session: AsyncSession) -> AuthRepository:
        return AuthRepository(session)

    @provide(scope=Scope.APP)
    def provide_zitadel_client(self, config: AuthConfig) -> ZitadelOidcClient:
        return ZitadelOidcClient(config)

    @provide(scope=Scope.APP)
    def provide_telegram_verifier(self, config: AuthConfig) -> TelegramAuthVerifier:
        return TelegramAuthVerifier(config)

    @provide(scope=Scope.APP)
    def provide_oidc_verifier(
        self,
        zitadel_client: ZitadelOidcClient,
        config: AuthConfig,
    ) -> OidcTokenVerifier:
        return OidcTokenVerifier(zitadel_client, config)

    @provide(scope=Scope.REQUEST)
    def provide_auth_service(
        self,
        repository: AuthRepository,
        telegram_verifier: TelegramAuthVerifier,
        oidc_verifier: OidcTokenVerifier,
    ) -> AuthService:
        return AuthService(
            repository=repository,
            telegram_verifier=telegram_verifier,
            oidc_verifier=oidc_verifier,
        )
