from .dto import AuthenticatedUser, AuthIdentity, AuthProvider, User, UserStatus, VerifiedIdentity
from .exceptions import (
    AuthError,
    IdentityConflict,
    IdentityNotFound,
    InvalidCredentials,
    LastIdentityRemoval,
    UnsupportedProvider,
    UserForbidden,
)
from .telegram import TelegramAuthVerifier
from .zitadel import OidcTokenVerifier, ZitadelOidcClient

__all__ = (
    "AuthError",
    "AuthIdentity",
    "AuthProvider",
    "AuthenticatedUser",
    "IdentityConflict",
    "IdentityNotFound",
    "InvalidCredentials",
    "LastIdentityRemoval",
    "OidcTokenVerifier",
    "TelegramAuthVerifier",
    "UnsupportedProvider",
    "User",
    "UserForbidden",
    "UserStatus",
    "VerifiedIdentity",
    "ZitadelOidcClient",
)
