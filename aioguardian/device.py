"""Define device info-related API endpoints."""
from typing import Callable


class Device:
    """Define the endpoint manager."""

    def __init__(self, execute_command: Callable) -> None:
        """Initialize."""
        self._execute_command = execute_command

    def diagnostics(self) -> dict:
        """Retrieve diagnostics info."""
        return self._execute_command(1)

    def factory_reset(self) -> dict:
        """Perform a factory reset on the device."""
        return self._execute_command(255)

    def ping(self) -> dict:
        """Ping the device."""
        return self._execute_command(0)

    def reboot(self) -> dict:
        """Reboot the device."""
        return self._execute_command(2)
