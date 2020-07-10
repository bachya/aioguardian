"""Define system commands."""
import asyncio
from typing import Any, Callable, Coroutine, Dict

import voluptuous as vol

from aioguardian.errors import CommandError
from aioguardian.helpers.command import Command
import aioguardian.helpers.config_validation as cv

PARAM_FILENAME: str = "filename"
PARAM_PORT: str = "port"
PARAM_URL: str = "url"

UPGRADE_FIRMWARE_PARAM_SCHEMA: vol.Schema = vol.Schema(
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
    """

    def __init__(self, execute_command: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._execute_command: Callable[..., Coroutine] = execute_command

    async def diagnostics(self, *, silent: bool = True) -> dict:
        """Retrieve diagnostics info.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.system_diagnostics, silent=silent)

    async def factory_reset(self, *, silent: bool = True) -> dict:
        """Perform a factory reset on the device.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.system_factory_reset, silent=silent)

    async def onboard_sensor_status(self, *, silent: bool = True) -> dict:
        """Retrieve status of the valve controller's onboard sensors.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(
            Command.system_onboard_sensor_status, silent=silent
        )

    async def ping(self, *, silent: bool = True) -> dict:
        """Ping the device.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.system_ping, silent=silent)

    async def reboot(self, *, silent: bool = True) -> dict:
        """Reboot the device.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        resp = await self._execute_command(Command.system_reboot, silent=silent)

        # The Guardian API docs indicate that the reboot will occur "3 seconds after
        # command is received" – in order to guard against errors from subsequent
        # commands while the reboot is occurring, we sleep for 3 seconds before
        # returning the response:
        await asyncio.sleep(3)

        return resp

    async def upgrade_firmware(
        self,
        *,
        url: str = None,
        port: int = None,
        filename: str = None,
        silent: bool = True,
    ) -> dict:
        """Upgrade the firmware on the device.

        :param url: The firmware file's optional URL
        :type url: ``str``
        :param port: The firmware file's optional port
        :type port: ``int``
        :param filename: The firmware file's optional filename
        :type filename: ``str``
        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        params: Dict[str, Any] = {}
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
            Command.system_upgrade_firmware, params=params, silent=silent
        )
