"""Define valve commands."""
import logging
from typing import Any, Awaitable, Callable, Dict, cast

from aioguardian.helpers.command import Command

_LOGGER = logging.getLogger(__name__)

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


class ValveCommands:
    """Define an object to manage valve commands.

    Note that this class shouldn't be instantiated directly; an instance of it will
    automatically be added to the :meth:`Client <aioguardian.Client>` (as
    ``client.valve``).
    """

    def __init__(self, execute_command: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._execute_command = execute_command

    async def close(self) -> Dict[str, Any]:
        """Close the valve.

        :rtype: ``dict``
        """
        data = await self._execute_command(Command.valve_close)
        return cast(Dict[str, Any], data)

    async def halt(self) -> Dict[str, Any]:
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
        data = await self._execute_command(Command.valve_halt)
        return cast(Dict[str, Any], data)

    async def open(self) -> Dict[str, Any]:
        """Open the valve.

        :rtype: ``dict``
        """
        data = await self._execute_command(Command.valve_open)
        return cast(Dict[str, Any], data)

    async def reset(self, *, silent: bool = True) -> Dict[str, Any]:
        """Reset the valve.

        This fully resets system motor diagnostics (including open/close count and
        lifetime average current draw) and cannot be undone.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        data = await self._execute_command(Command.valve_reset, silent=silent)
        return cast(Dict[str, Any], data)

    async def status(self, *, silent: bool = True) -> Dict[str, Any]:
        """Retrieve status of the valve.

        In the payload that is returned, the ``state`` attribute of the valve can be any
        one of the following:

            * ``closed``
            * ``closing``
            * ``default``
            * ``finish_closing``
            * ``finish_opening``
            * ``free_spin``
            * ``halted``
            * ``opened``
            * ``opening``
            * ``stalled``
            * ``start_closing``
            * ``start_halt``
            * ``start_opening``

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        data = await self._execute_command(Command.valve_status, silent=silent)
        data["data"]["state"] = VALVE_STATE_MAPPING[data["data"]["state"]]
        return cast(Dict[str, Any], data)
