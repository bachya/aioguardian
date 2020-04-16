"""Define command helpers."""
from enum import Enum


class Command(Enum):
    """Define a Guardian UDP command mapping."""

    ping = 0
    diagnostics = 1
    reboot = 2
    upgrade_firmware = 4
    factory_reset = 255
