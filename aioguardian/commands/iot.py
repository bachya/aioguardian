"""Define IOT commands."""
from typing import Callable, Coroutine

from aioguardian.helpers.command import Command


class IOTCommands:  # pylint: disable=too-few-public-methods
    """Define an object to manage IOT commands.

    Note that this class shouldn't be instantiated directly; an instance of it will
    automatically be added to the :meth:`Client <aioguardian.Client>` (as
    ``client.iot``).
    """

    def __init__(self, execute_command: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._execute_command: Callable[..., Coroutine] = execute_command

    async def publish_state(self, *, silent: bool = True) -> dict:
        """Publish the device's complete state to the Guardian cloud.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.iot_publish_state, silent=silent)
