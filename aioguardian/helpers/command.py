"""Define command helpers."""
from enum import Enum


class Command(Enum):
    """Define a Guardian UDP command mapping."""

    ping = 0
    diagnostics = 1
    reboot = 2
    upgrade_firmware = 4
    valve_status = 16
    valve_open = 17
    valve_close = 18
    sensor_status = 80
    factory_reset = 255
