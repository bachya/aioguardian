"""Define exception types for ``aioguardian``."""
from typing import Dict

ERROR_CODE_MAPPING: Dict[int, str] = {
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
