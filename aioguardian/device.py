"""Define device info-related API endpoints."""
from typing import Callable


class Device:  # pylint: disable=too-few-public-methods
    """Define the endpoint manager."""

    def __init__(self, execute_command: Callable):
        """Initialize."""
        self._execute_command = execute_command

    def ping(self):
        """Ping the device."""
        return self._execute_command(0)
