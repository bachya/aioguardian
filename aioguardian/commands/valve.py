"""Define valve commands."""
import logging
from collections.abc import Awaitable, Callable
from typing import Any, cast

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

    Args:
        execute_command: The execute_command method from the Client object.
    """

    def __init__(self, execute_command: Callable[..., Awaitable]) -> None:
        """Initialize.

        Args:
            execute_command: The execute_command method from the Client object.
        """
        self._execute_command = execute_command

    async def close(self) -> dict[str, Any]:
        """Close the valve.

        Returns:
            An API response payload.
        """
        data = await self._execute_command(Command.VALVE_CLOSE)
        return cast(dict[str, Any], data)

    async def halt(self) -> dict[str, Any]:
        """Halt the valve.

        Note that calling this method will cause the device to no longer respond to leak
        events; therefore, it is not recommended to leave the device in a "halted" state
        indefinitely.

        Returns:
            An API response payload.
        """
        _LOGGER.warning(
            "The device will not respond to leak events while in a halted state. It is "
            "recommended that you call valve_close() or valve_open() as soon as "
            "possible."
        )
        data = await self._execute_command(Command.VALVE_HALT)
        return cast(dict[str, Any], data)

    async def open(self) -> dict[str, Any]:
        """Open the valve.

        Returns:
            An API response payload.
        """
        data = await self._execute_command(Command.VALVE_OPEN)
        return cast(dict[str, Any], data)

    async def reset(self, *, silent: bool = True) -> dict[str, Any]:
        """Reset the valve.

        This fully resets system motor diagnostics (including open/close count and
        lifetime average current draw) and cannot be undone.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        data = await self._execute_command(Command.VALVE_RESET, silent=silent)
        return cast(dict[str, Any], data)

    async def status(self, *, silent: bool = True) -> dict[str, Any]:
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

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        data = await self._execute_command(Command.VALVE_STATUS, silent=silent)
        data["data"]["state"] = VALVE_STATE_MAPPING[data["data"]["state"]]
        return cast(dict[str, Any], data)
