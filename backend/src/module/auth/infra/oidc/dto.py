import datetime as dt
from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class UserStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    BANNED = "banned"


class AuthProvider(StrEnum):
    TELEGRAM = "telegram"
    ZITADEL = "zitadel"
    CASDOOR = "casdoor"


@dataclass(frozen=True)
class User:
    id: UUID
    status: UserStatus
    created_at: dt.datetime
    updated_at: dt.datetime


@dataclass(frozen=True)
class AuthIdentity:
    id: UUID
    user_id: UUID
    provider: AuthProvider
    subject: str
    email: str | None
    username: str | None
    created_at: dt.datetime
    updated_at: dt.datetime


@dataclass(frozen=True)
class VerifiedIdentity:
    provider: AuthProvider
    subject: str
    email: str | None = None
    username: str | None = None


@dataclass(frozen=True)
class AuthenticatedUser:
    user_id: UUID
    identity_id: UUID
    provider: str
    subject: str
    status: str
