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

    Note that this class shouldn't be instantiated directly; it will be instantiated as
    appropriate when creating a :meth:`aioguardian.Client`.
    """

    def __init__(self, execute_command: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._execute_command: Callable[..., Coroutine] = execute_command

    async def diagnostics(self) -> dict:
        """Retrieve diagnostics info.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.diagnostics)

    async def factory_reset(self) -> dict:
        """Perform a factory reset on the device.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.factory_reset)

    async def ping(self) -> dict:
        """Ping the device.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.ping)

    async def publish_state(self) -> dict:
        """Publish the device's complete state to the Guardian cloud.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.publish_state)

    async def reboot(self) -> dict:
        """Reboot the device.

        :rtype: ``dict``
        """
        resp = await self._execute_command(Command.reboot)

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
    ) -> dict:
        """Upgrade the firmware on the device.

        :param url: The firmware file's URL
        :type url: ``str``
        :param port: The firmware file's port
        :type port: ``int``
        :param filename: The firmware file's filename
        :type filename: ``str``
        :rtype: ``dict``
        """
        params = {PARAM_URL: url, PARAM_PORT: port, PARAM_FILENAME: filename}

        try:
            UPGRADE_FIRMWARE_PARAM_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        return await self._execute_command(Command.upgrade_firmware, params=params)

    async def wifi_configure(self, ssid: str, password: str) -> dict:
        """Configure the device to a wireless network.

        :param ssid: The SSID to connect to
        :type ssid: ``str``
        :param password: The SSID's password
        :type password: ``str``
        :rtype: ``dict``
        """
        params = {PARAM_SSID: ssid, PARAM_PASSWORD: password}

        try:
            WIFI_CONFIGURE_PARAM_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        return await self._execute_command(Command.wifi_configure, params=params)

    async def wifi_disable_ap(self) -> dict:
        """Disable the device's onboard WiFi access point.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.wifi_disable_ap)

    async def wifi_enable_ap(self) -> dict:
        """Enable the device's onboard WiFi access point.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.wifi_enable_ap)

    async def wifi_reset(self) -> dict:
        """Erase and reset all WiFi settings.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.wifi_reset)

    async def wifi_status(self) -> dict:
        """Return the current WiFi status of the device.

        :rtype: ``dict``
        """
        return await self._execute_command(Command.wifi_status)
