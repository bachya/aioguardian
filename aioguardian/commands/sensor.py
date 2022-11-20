"""Define sensor commands."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

import voluptuous as vol

import aioguardian.helpers.config_validation as cv
from aioguardian.errors import CommandError
from aioguardian.helpers.command import Command

PARAM_UID = "uid"

PAIRED_SENSOR_UID_SCHEMA: vol.Schema = vol.Schema(
    {vol.Required(PARAM_UID): vol.All(cv.alphanumeric, vol.Length(max=12))}
)


class SensorCommands:
    """Define an object to manage sensor commands.

    Note that this class shouldn't be instantiated directly; an instance of it will
    automatically be added to the :meth:`Client <aioguardian.Client>` (as
    ``client.sensor``).

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

    async def pair_dump(self, *, silent: bool = True) -> dict[str, Any]:
        """Dump information on all paired sensors.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        return await self._execute_command(Command.SENSOR_PAIR_DUMP, silent=silent)

    async def pair_sensor(self, uid: str, *, silent: bool = True) -> dict[str, Any]:
        """Pair a new sensor to the device.

        Args:
            uid: A UID of a Guardian paired sensor.
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.

        Raises:
            CommandError: Raised when invalid parameters are provided.
        """
        params = {PARAM_UID: uid}

        try:
            PAIRED_SENSOR_UID_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        return await self._execute_command(
            Command.SENSOR_PAIR_SENSOR, params=params, silent=silent
        )

    async def paired_sensor_status(
        self, uid: str, *, silent: bool = True
    ) -> dict[str, Any]:
        """Get the status (leak, temperature, etc.) of a paired sensor.

        Args:
            uid: A UID of a Guardian paired sensor.
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.

        Raises:
            CommandError: Raised when invalid parameters are provided.
        """
        params = {PARAM_UID: uid}

        try:
            PAIRED_SENSOR_UID_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        return await self._execute_command(
            Command.SENSOR_PAIRED_SENSOR_STATUS, params=params, silent=silent
        )

    async def unpair_sensor(self, uid: str, *, silent: bool = True) -> dict[str, Any]:
        """Unpair a sensor from the device.

        Args:
            uid: A UID of a Guardian paired sensor.
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.

        Raises:
            CommandError: Raised when invalid parameters are provided.
        """
        params = {PARAM_UID: uid}

        try:
            PAIRED_SENSOR_UID_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        return await self._execute_command(
            Command.SENSOR_UNPAIR_SENSOR, params=params, silent=silent
        )
