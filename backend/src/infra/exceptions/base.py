class ApplicationError(Exception):
    """Base Application Exception."""

    @property
    def title(self) -> str:
        return "An application error occurred"
