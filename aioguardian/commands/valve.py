"""async define onboard valve-related API endpoints."""
import logging
from typing import Callable, Coroutine, Dict

from aioguardian.helpers.command import Command

_LOGGER = logging.getLogger(__name__)

VALVE_STATE_MAPPING: Dict[int, str] = {
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


class Valve:
    """Define an object to manage valve-related commands.

    Note that this class shouldn't be instantiated directly; it will be instantiated as
    appropriate when creating a :meth:`aioguardian.Client`.
    """

    def __init__(self, execute_command: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._execute_command: Callable[..., Coroutine] = execute_command

    async def valve_close(self) -> dict:
        """Close the valve.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.valve_close)

    async def valve_halt(self) -> dict:
        """Halt the valve.

        Note that calling this method will cause the device to no longer respond to leak
        events; therefore, it is not recommended to leave the device in a "halted" state
        indefinitely.

        :rtype: ``dict``
        """
        _LOGGER.warning(
            "The device will not respond to leak events while in a halted state. It is "
            "recommended that you call valve_close() or valve_open() as soon as "
            "possible."
        )
        return await self._execute_command(Command.valve_halt)

    async def valve_open(self) -> dict:
        """Open the valve.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.valve_open)

    async def valve_reset(self) -> dict:
        """Reset the valve.

        This fully resets system motor diagnostics including open/close count and
        lifetime average current draw and cannot be undone.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.valve_reset)

    async def valve_status(self) -> dict:
        """Retrieve status of the valve.

        :rtype: ``dict``
        """
        resp = await self._execute_command(Command.valve_status)
        resp["data"]["state"] = VALVE_STATE_MAPPING[resp["data"]["state"]]
        return resp
