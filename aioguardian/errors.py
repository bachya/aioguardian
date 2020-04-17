"""Define exception types for ``aioguardian``."""
from typing import Dict

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


ERROR_CODE_MAPPING: Dict[int, str] = {
    17: "valve_already_opened",
    18: "valve_already_closed",
    19: "valve_already_stopped",
    20: "valve_moving",
}


def _raise_on_command_error(command: Command, data: dict) -> None:
    """Examine a data response and raise errors appropriately.

    :param command: The command that was run
    :type command: :meth:`aioguardian.helpers.command.Command`
    :param data: The response data from running the command
    :type params: ``dict``
    """
    if data.get("status") == "ok":
        return

    if data.get("error_code") in ERROR_CODE_MAPPING:
        raise CommandError(
            f"{command.name} command failed: {ERROR_CODE_MAPPING[data['error_code']]}"
        )

    raise CommandError(f"{command.name} command failed (response: {data})")
