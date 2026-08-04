import datetime as dt
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, ForeignKey, MetaData, String, Table, UniqueConstraint, delete, insert, select
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from module.auth.infra.oidc import (
    AuthIdentity,
    AuthProvider,
    IdentityConflict,
    IdentityNotFound,
    LastIdentityRemoval,
    User,
    UserStatus,
    VerifiedIdentity,
)

auth_metadata = MetaData()

auth_users_table = Table(
    "auth_users",
    auth_metadata,
    Column("id", PgUUID(as_uuid=True), primary_key=True),
    Column("status", String(32), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)

auth_identities_table = Table(
    "auth_identities",
    auth_metadata,
    Column("id", PgUUID(as_uuid=True), primary_key=True),
    Column("user_id", PgUUID(as_uuid=True), ForeignKey("auth_users.id", ondelete="CASCADE"), nullable=False),
    Column("provider", String(32), nullable=False),
    Column("subject", String(255), nullable=False),
    Column("email", String(320), nullable=True),
    Column("username", String(255), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    UniqueConstraint("provider", "subject", name="uq_auth_identities_provider_subject"),
)


class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user(self, user_id: UUID) -> User | None:
        row = (
            (
                await self._session.execute(
                    select(auth_users_table).where(auth_users_table.c.id == user_id),
                )
            )
            .mappings()
            .one_or_none()
        )
        if row is None:
            return None
        return _user_from_row(row)

    async def login_or_create_user(self, identity: VerifiedIdentity) -> tuple[User, AuthIdentity]:
        auth_identity = await self.get_identity(identity.provider, identity.subject)
        if auth_identity is not None:
            user = await self.get_user(auth_identity.user_id)
            if user is None:
                msg = "Auth identity is linked to missing user"
                raise IdentityNotFound(msg)
            return user, auth_identity

        now = _utc_now()
        user = User(
            id=uuid4(),
            status=UserStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        auth_identity = _build_identity(user.id, identity, now)

        await self._session.execute(
            insert(auth_users_table).values(
                id=user.id,
                status=user.status.value,
                created_at=user.created_at,
                updated_at=user.updated_at,
            ),
        )
        await self._insert_identity(auth_identity)
        await self._session.commit()
        return user, auth_identity

    async def get_identity(self, provider: AuthProvider, subject: str) -> AuthIdentity | None:
        row = (
            (
                await self._session.execute(
                    select(auth_identities_table).where(
                        auth_identities_table.c.provider == provider.value,
                        auth_identities_table.c.subject == subject,
                    ),
                )
            )
            .mappings()
            .one_or_none()
        )
        if row is None:
            return None
        return _identity_from_row(row)

    async def link_identity(self, user_id: UUID, identity: VerifiedIdentity) -> AuthIdentity:
        existing_identity = await self.get_identity(identity.provider, identity.subject)
        if existing_identity is not None:
            if existing_identity.user_id != user_id:
                msg = "Auth identity is already linked to another user"
                raise IdentityConflict(msg)
            return existing_identity

        auth_identity = _build_identity(user_id, identity, _utc_now())
        await self._insert_identity(auth_identity)
        await self._session.commit()
        return auth_identity

    async def list_identities(self, user_id: UUID) -> list[AuthIdentity]:
        rows = (
            (
                await self._session.execute(
                    select(auth_identities_table).where(auth_identities_table.c.user_id == user_id),
                )
            )
            .mappings()
            .all()
        )
        return [_identity_from_row(row) for row in rows]

    async def unlink_identity(self, user_id: UUID, identity_id: UUID) -> None:
        identities = await self.list_identities(user_id)
        identity = next((item for item in identities if item.id == identity_id), None)
        if identity is None:
            msg = "Auth identity was not found"
            raise IdentityNotFound(msg)
        if len(identities) <= 1:
            msg = "Cannot remove the last login method"
            raise LastIdentityRemoval(msg)

        await self._session.execute(
            delete(auth_identities_table).where(
                auth_identities_table.c.id == identity_id,
                auth_identities_table.c.user_id == user_id,
            ),
        )
        await self._session.commit()

    async def _insert_identity(self, identity: AuthIdentity) -> None:
        await self._session.execute(
            insert(auth_identities_table).values(
                id=identity.id,
                user_id=identity.user_id,
                provider=identity.provider.value,
                subject=identity.subject,
                email=identity.email,
                username=identity.username,
                created_at=identity.created_at,
                updated_at=identity.updated_at,
            ),
        )


def _build_identity(user_id: UUID, identity: VerifiedIdentity, now: dt.datetime) -> AuthIdentity:
    return AuthIdentity(
        id=uuid4(),
        user_id=user_id,
        provider=identity.provider,
        subject=identity.subject,
        email=identity.email,
        username=identity.username,
        created_at=now,
        updated_at=now,
    )


def _user_from_row(row: RowMapping) -> User:
    return User(
        id=row["id"],
        status=UserStatus(row["status"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def _identity_from_row(row: RowMapping) -> AuthIdentity:
    return AuthIdentity(
        id=row["id"],
        user_id=row["user_id"],
        provider=AuthProvider(row["provider"]),
        subject=row["subject"],
        email=row["email"],
        username=row["username"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def _utc_now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)
