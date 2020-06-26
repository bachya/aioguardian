"""Define command helpers."""
from enum import Enum

from aioguardian.errors import CommandError


class Command(Enum):
    """Define a Guardian UDP command mapping."""

    iot_publish_state = 65
    sensor_pair_dump = 48
    sensor_pair_sensor = 49
    sensor_paired_sensor_status = 51
    sensor_unpair_sensor = 50
    system_diagnostics = 1
    system_factory_reset = 255
    system_onboard_sensor_status = 80
    system_ping = 0
    system_reboot = 2
    system_upgrade_firmware = 4
    valve_close = 18
    valve_halt = 19
    valve_open = 17
    valve_reset = 20
    valve_status = 16
    wifi_configure = 34
    wifi_disable_ap = 36
    wifi_enable_ap = 35
    wifi_list = 38
    wifi_reset = 33
    wifi_scan = 37
    wifi_status = 32


def get_command_from_name(command_name: str) -> Command:
    """Return the command for a particular name.

    :param command_name: The command name to search for
    :type command_name: ``str``
    :rtype: :meth:`aioguardian.helpers.command.Command`
    """
    try:
        command = Command[command_name]
    except KeyError:
        raise CommandError(f"Unknown command name: {command_name}") from None
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
        raise CommandError(f"Unknown command code: {command_code}") from None
    return command
