"""Define system commands."""
from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

import voluptuous as vol

import aioguardian.helpers.config_validation as cv
from aioguardian.errors import CommandError
from aioguardian.helpers.command import Command

PARAM_FILENAME = "filename"
PARAM_PORT = "port"
PARAM_URL = "url"

UPGRADE_FIRMWARE_PARAM_SCHEMA = vol.Schema(
    {
        vol.Optional(PARAM_URL): vol.All(cv.url, vol.Length(max=256)),
        vol.Optional(PARAM_PORT): int,
        vol.Optional(PARAM_FILENAME): vol.All(str, vol.Length(max=48)),
    }
)


class SystemCommands:
    """Define an object to manage system commands.

    Note that this class shouldn't be instantiated directly; an instance of it will
    automatically be added to the :meth:`Client <aioguardian.Client>` (as
    ``client.system``).

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

    async def diagnostics(self, *, silent: bool = True) -> dict[str, Any]:
        """Retrieve diagnostics info.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        return await self._execute_command(Command.SYSTEM_DIAGNOSTICS, silent=silent)

    async def factory_reset(self, *, silent: bool = True) -> dict[str, Any]:
        """Perform a factory reset on the device.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        return await self._execute_command(Command.SYSTEM_FACTORY_RESET, silent=silent)

    async def onboard_sensor_status(self, *, silent: bool = True) -> dict[str, Any]:
        """Retrieve status of the valve controller's onboard sensors.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        return await self._execute_command(
            Command.SYSTEM_ONBOARD_SENSOR_STATUS, silent=silent
        )

    async def ping(self, *, silent: bool = True) -> dict[str, Any]:
        """Ping the device.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        return await self._execute_command(Command.SYSTEM_PING, silent=silent)

    async def reboot(self, *, silent: bool = True) -> dict[str, Any]:
        """Reboot the device.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        data = await self._execute_command(Command.SYSTEM_REBOOT, silent=silent)

        # The Guardian API docs indicate that the reboot will occur "3 seconds after
        # command is received" – in order to guard against errors from subsequent
        # commands while the reboot is occurring, we sleep for 3 seconds before
        # returning the response:
        await asyncio.sleep(3)

        return data

    async def upgrade_firmware(
        self,
        *,
        url: str | None = None,
        port: int | None = None,
        filename: str | None = None,
        silent: bool = True,
    ) -> dict[str, Any]:
        """Upgrade the firmware on the device.

        Args:
            url: A Guardian-provided URL that hosts firmware files.
            port: A port at the Guardian-provided URL that can be accessed.
            filename: A firmware filename.
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.

        Raises:
            CommandError: Raised when invalid parameters are provided.
        """
        params: dict[str, int | str] = {}
        if url:
            params["url"] = url
        if port:
            params["port"] = port
        if filename:
            params["filename"] = filename

        try:
            UPGRADE_FIRMWARE_PARAM_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        return await self._execute_command(
            Command.SYSTEM_UPGRADE_FIRMWARE, params=params, silent=silent
        )
