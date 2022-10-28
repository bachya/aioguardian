"""Define command helpers."""
from enum import Enum

from aioguardian.errors import CommandError


class Command(Enum):
    """Define a Guardian UDP command mapping."""

    IOT_PUBLISH_STATE = 65
    SENSOR_PAIR_DUMP = 48
    SENSOR_PAIR_SENSOR = 49
    SENSOR_PAIRED_SENSOR_STATUS = 51
    SENSOR_UNPAIR_SENSOR = 50
    SYSTEM_DIAGNOSTICS = 1
    SYSTEM_FACTORY_RESET = 255
    SYSTEM_ONBOARD_SENSOR_STATUS = 80
    SYSTEM_PING = 0
    SYSTEM_REBOOT = 2
    SYSTEM_UPGRADE_FIRMWARE = 4
    VALVE_CLOSE = 18
    VALVE_HALT = 19
    VALVE_OPEN = 17
    VALVE_RESET = 20
    VALVE_STATUS = 16
    WIFI_CONFIGURE = 34
    WIFI_DISABLE_AP = 36
    WIFI_ENABLE_AP = 35
    WIFI_LIST = 38
    WIFI_RESET = 33
    WIFI_SCAN = 37
    WIFI_STATUS = 32


def get_command_from_name(command_name: str) -> Command:
    """Return the command for a particular name.

    Args:
        command_name: The command string to parse into a Command.

    Returns:
        A Command object.

    Raises:
        CommandError: Raised when an unknown command is encountered.
    """
    try:
        command = Command[command_name]
    except KeyError:
        raise CommandError(f"Unknown command name: {command_name}") from None
    return command


def get_command_from_code(command_code: int) -> Command:
    """Return the command for a particular code.

    Args:
        command_code: The raw command code to parse into a Command.

    Returns:
        A Command object.

    Raises:
        CommandError: Raised when an unknown command is encountered.
    """
    try:
        command = Command(command_code)
    except ValueError:
        raise CommandError(f"Unknown command code: {command_code}") from None
    return command
