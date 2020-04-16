"""async define onboard valve-related API endpoints."""
from enum import Enum
from typing import Callable, Coroutine

from aioguardian.helpers.command import Command


class ValveState(Enum):
    """Define a representation of the valve's state."""

    default = 0
    start_opening = 1
    opening = 2
    finish_opening = 3
    opened = 4
    start_closing = 5
    closing = 6
    finish_closing = 7
    closed = 8
    start_halt = 9
    stalled = 10
    free_spin = 11
    halted = 12


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
        data = await self._execute_command(Command.valve_status)
        data["data"]["state"] = ValveState(data["data"]["state"])
        return data
