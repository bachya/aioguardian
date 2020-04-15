"""Define device info-related API endpoints."""
from typing import Callable, Coroutine


class Device:  # pylint: disable=too-few-public-methods
    """Define the endpoint manager."""

    def __init__(
        self,
        async_execute_command: Callable[..., Coroutine],
        create_or_run_future: Callable,
    ):
        """Initialize."""
        self._async_execute_command = async_execute_command
        self._create_or_run_future = create_or_run_future

    def ping(self):
        """Ping the device."""
        return self._create_or_run_future(self._async_execute_command(0))
