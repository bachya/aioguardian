"""async define onboard valve-related API endpoints."""
from typing import Callable, Coroutine

from aioguardian.helpers.command import Command

VALVE_STATE_MAPPING = {
    0: "default",
    1: "start_opening",
    2: "opening",
    3: "finish_opening",
    4: "opened",
    5: "start_closing",
    6: "closing",
    7: "finish_closing",
    8: "closed",
    9: "start_halt",
    10: "stalled",
    11: "free_spin",
    12: "halted",
}


class Valve:  # pylint: disable=too-few-public-methods
    """Define the manager object.

    Note that this class shouldn't be instantiated directly; it will be instantiated as
    appropriate when creating a :meth:`aioguardian.client.Client`.
    """

    def __init__(self, execute_command: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._execute_command = execute_command

    async def valve_open(self) -> dict:
        """Open the valve.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.valve_open)

    async def valve_status(self) -> dict:
        """Retrieve status of the valve.

        :rtype: ``dict``
        """
        resp = await self._execute_command(Command.valve_status)
        resp["data"]["state"] = VALVE_STATE_MAPPING[resp["data"]["state"]]
        return resp
