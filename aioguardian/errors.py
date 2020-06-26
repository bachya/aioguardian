"""Define exception types for ``aioguardian``."""
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from aioguardian.helpers.command import Command

ERROR_CODE_MAPPING: Dict[int, str] = {
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


def _raise_on_command_error(command: "Command", data: dict) -> None:
    """Examine a data response and raise errors appropriately.

    :param command: The command that was run
    :type command: :meth:`aioguardian.helpers.command.Command`
    :param data: The response data from running the command
    :type params: ``dict``
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
