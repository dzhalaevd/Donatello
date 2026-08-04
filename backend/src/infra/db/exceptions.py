from infra.exceptions import ApplicationError


class UnexpectedError(ApplicationError):
    pass


class CommitError(UnexpectedError):
    pass


class RollbackError(UnexpectedError):
    pass
