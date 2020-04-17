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
