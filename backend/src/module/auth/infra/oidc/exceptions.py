class ZitadelAuthError(Exception):
    pass


class ZitadelTokenError(ZitadelAuthError):
    pass


class ZitadelConfigurationError(ZitadelAuthError):
    pass


class AuthError(Exception):
    pass


class InvalidCredentials(AuthError):
    pass


class UnsupportedProvider(AuthError):
    pass


class IdentityConflict(AuthError):
    pass


class UserForbidden(AuthError):
    pass


class LastIdentityRemoval(AuthError):
    pass


class IdentityNotFound(AuthError):
    pass
