"""Define IOT commands."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from aioguardian.helpers.command import Command


class IOTCommands:  # pylint: disable=too-few-public-methods
    """Define an object to manage IOT commands.

    Note that this class shouldn't be instantiated directly; an instance of it will
    automatically be added to the :meth:`Client <aioguardian.Client>` (as
    ``client.iot``).

    Args:
        execute_command: The execute_command method from the Client object.
    """

    def __init__(
        self, execute_command: Callable[..., Awaitable[dict[str, Any]]]
    ) -> None:
        """Initialize.

        Args:
            execute_command: The execute_command method from the Client object.
        """
        self._execute_command = execute_command

    async def publish_state(self, *, silent: bool = True) -> dict[str, Any]:
        """Publish the device's complete state to the Guardian cloud.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        return await self._execute_command(Command.IOT_PUBLISH_STATE, silent=silent)
