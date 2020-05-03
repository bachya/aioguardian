"""Define command helpers."""
from enum import Enum

from aioguardian.errors import CommandError


class Command(Enum):
    """Define a Guardian UDP command mapping."""

    ping = 0
    diagnostics = 1
    reboot = 2
    upgrade_firmware = 4
    valve_status = 16
    valve_open = 17
    valve_close = 18
    valve_halt = 19
    valve_reset = 20
    wifi_status = 32
    wifi_reset = 33
    wifi_configure = 34
    wifi_enable_ap = 35
    wifi_disable_ap = 36
    pair_dump = 48
    pair_sensor = 49
    publish_state = 65
    sensor_status = 80
    factory_reset = 255


def get_command_from_name(command_name: str) -> Command:
    """Return the command for a particular name.

    :param command_name: The command name to search for
    :type command_name: ``str``
    :rtype: :meth:`aioguardian.helpers.command.Command`
    """
    try:
        command = Command[command_name]
    except KeyError:
        raise CommandError(f"Unknown command name: {command_name}")
    return command


def get_command_from_code(command_code: int) -> Command:
    """Return the command for a particular code.

    :param command_code: The command code to search for
    :type command_code: ``int``
    :rtype: :meth:`aioguardian.helpers.command.Command`
    """
    try:
        command = Command(command_code)
    except ValueError:
        raise CommandError(f"Unknown command code: {command_code}")
    return command
