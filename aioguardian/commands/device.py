"""async define device info-related API endpoints."""
import asyncio
from typing import Callable, Coroutine

import voluptuous as vol

from aioguardian.errors import CommandError
from aioguardian.helpers.command import Command
import aioguardian.helpers.config_validation as cv

DEFAULT_FIRMWARE_UPGRADE_FILENAME: str = "latest.bin"
DEFAULT_FIRMWARE_UPGRADE_PORT: int = 443
DEFAULT_FIRMWARE_UPGRADE_URL: str = "https://repo.guardiancloud.services/gvc/fw"

PARAM_FILENAME: str = "filename"
PARAM_PASSWORD: str = "password"
PARAM_PORT: str = "port"
PARAM_SSID: str = "ssid"
PARAM_URL: str = "url"

UPGRADE_FIRMWARE_PARAM_SCHEMA: vol.Schema = vol.Schema(
    {
        vol.Required(PARAM_URL): vol.All(cv.url, vol.Length(max=256)),
        vol.Required(PARAM_PORT): int,
        vol.Required(PARAM_FILENAME): vol.All(str, vol.Length(max=48)),
    }
)

WIFI_CONFIGURE_PARAM_SCHEMA: vol.Schema = vol.Schema(
    {
        vol.Required(PARAM_SSID): vol.All(str, vol.Length(max=36)),
        vol.Required(PARAM_PASSWORD): vol.All(str, vol.Length(max=64)),
    }
)


class Device:
    """Define an object to manage device-related commands.

    Note that this class shouldn't be instantiated directly; an instance of it will
    automatically be added to the :meth:`Client <aioguardian.Client>` (as
    ``client.device``).
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
        return await self._execute_command(Command.diagnostics, silent=silent)

    async def factory_reset(self, *, silent: bool = True) -> dict:
        """Perform a factory reset on the device.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.factory_reset, silent=silent)

    async def ping(self, *, silent: bool = True) -> dict:
        """Ping the device.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.ping, silent=silent)

    async def publish_state(self, *, silent: bool = True) -> dict:
        """Publish the device's complete state to the Guardian cloud.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.publish_state, silent=silent)

    async def reboot(self, *, silent: bool = True) -> dict:
        """Reboot the device.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        resp = await self._execute_command(Command.reboot, silent=silent)

        # The Guardian API docs indicate that the reboot will occur "3 seconds after
        # command is received" – in order to guard against errors from subsequent
        # commands while the reboot is occurring, we sleep for 3 seconds before
        # returning the response:
        await asyncio.sleep(3)

        return resp

    async def upgrade_firmware(
        self,
        *,
        url: str = DEFAULT_FIRMWARE_UPGRADE_URL,
        port: int = DEFAULT_FIRMWARE_UPGRADE_PORT,
        filename: str = DEFAULT_FIRMWARE_UPGRADE_FILENAME,
        silent: bool = True,
    ) -> dict:
        """Upgrade the firmware on the device.

        :param url: The firmware file's URL
        :type url: ``str``
        :param port: The firmware file's port
        :type port: ``int``
        :param filename: The firmware file's filename
        :type filename: ``str``
        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        params = {PARAM_URL: url, PARAM_PORT: port, PARAM_FILENAME: filename}

        try:
            UPGRADE_FIRMWARE_PARAM_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        return await self._execute_command(
            Command.upgrade_firmware, params=params, silent=silent
        )

    async def wifi_configure(
        self, ssid: str, password: str, *, silent: bool = True
    ) -> dict:
        """Configure the device to a wireless network.

        :param ssid: The SSID to connect to
        :type ssid: ``str``
        :param password: The SSID's password
        :type password: ``str``
        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        params = {PARAM_SSID: ssid, PARAM_PASSWORD: password}

        try:
            WIFI_CONFIGURE_PARAM_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        return await self._execute_command(
            Command.wifi_configure, params=params, silent=silent
        )

    async def wifi_disable_ap(self, *, silent: bool = True) -> dict:
        """Disable the device's onboard WiFi access point.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.wifi_disable_ap, silent=silent)

    async def wifi_enable_ap(self, *, silent: bool = True) -> dict:
        """Enable the device's onboard WiFi access point.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.wifi_enable_ap, silent=silent)

    async def wifi_reset(self, *, silent: bool = True) -> dict:
        """Erase and reset all WiFi settings.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.wifi_reset, silent=silent)

    async def wifi_status(self, *, silent: bool = True) -> dict:
        """Return the current WiFi status of the device.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.wifi_status, silent=silent)
