"""Define exception types for aioguardian."""
from aioguardian.helpers.command import Command


class GuardianError(Exception):
    """Define a base error from which all others inherit."""

    pass


class CommandError(GuardianError):
    """Define an general error for commands with issues."""

    pass


class SocketError(GuardianError):
    """Define an error related to UDP socket issues."""

    pass


def raise_on_command_error(command: Command, data: dict) -> None:
    """Examine a data response and raise errors appropriately."""
    if data.get("status") == "ok":
        return

    raise CommandError(f"{command.name} command failed (response: {data})")
