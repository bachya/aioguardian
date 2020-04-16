"""async define onboard valve-related API endpoints."""
from typing import Callable, Coroutine

from aioguardian.helpers.command import Command


class Valve:  # pylint: disable=too-few-public-methods
    """Define the manager object.

    Note that this class shouldn't be instantiated directly; it will be instantiated as
    appropriate when creating a :meth:`aioguardian.client.Client`.
    """

    def __init__(self, execute_command: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._execute_command = execute_command

    async def valve_status(self) -> dict:
        """Retrieve status of the valve.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.valve_status)
