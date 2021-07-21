"""Define IOT commands."""
from typing import Any, Awaitable, Callable, Dict, cast

from aioguardian.helpers.command import Command


class IOTCommands:  # pylint: disable=too-few-public-methods
    """Define an object to manage IOT commands.

    Note that this class shouldn't be instantiated directly; an instance of it will
    automatically be added to the :meth:`Client <aioguardian.Client>` (as
    ``client.iot``).
    """

    def __init__(self, execute_command: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._execute_command = execute_command

    async def publish_state(self, *, silent: bool = True) -> Dict[str, Any]:
        """Publish the device's complete state to the Guardian cloud.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        data = await self._execute_command(Command.iot_publish_state, silent=silent)
        return cast(Dict[str, Any], data)
