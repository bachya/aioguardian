"""Define exception types for ``aioguardian``."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aioguardian.helpers.command import Command

ERROR_CODE_MAPPING = {
    3: "sensor_not_paired",
    5: "sensor_error_loading",
    17: "valve_already_opened",
    18: "valve_already_closed",
    19: "valve_already_stopped",
    20: "valve_moving",
}


class GuardianError(Exception):
    """Define a base error from which all others inherit."""

    pass


class CommandError(GuardianError):
    """Define an error related to commands (invalid commands, invalid params, etc.)."""

    pass


class SocketError(GuardianError):
    """Define an error related to UDP socket issues."""

    pass


def _raise_on_command_error(command: Command, data: dict[str, Any]) -> None:
    """Examine a data response and raise errors appropriately.

    Args:
        command: The command to execute.
        data: An API response payload.o

    Raises:
        CommandError: Raised when a command fails for any reason.
    """
    if data.get("status") == "ok":
        return

    # If we know exactly why the command failed, raise that error:
    if data.get("error_code") in ERROR_CODE_MAPPING:
        raise CommandError(
            f"{command.name} command failed: {ERROR_CODE_MAPPING[data['error_code']]}"
        )

    # Last resort, return a generic error with the response payload:
    raise CommandError(f"{command.name} command failed (response: {data})")
