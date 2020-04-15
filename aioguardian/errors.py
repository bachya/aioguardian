"""Define exception types for aioguardian."""


class GuardianError(Exception):
    """Define a base error from which all others inherit."""

    pass


class RequestError(GuardianError):
    """Define an error related requests that return error responses."""

    pass


class SocketError(GuardianError):
    """Define an error related to UDP socket issues."""

    pass
