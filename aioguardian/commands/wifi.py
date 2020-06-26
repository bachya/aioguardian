"""Define WiFi commands."""
import logging
from typing import Callable, Coroutine

import voluptuous as vol

from aioguardian.errors import CommandError
from aioguardian.helpers.command import Command

_LOGGER = logging.getLogger(__name__)

PARAM_PASSWORD: str = "password"
PARAM_SSID: str = "ssid"

WIFI_CONFIGURE_PARAM_SCHEMA: vol.Schema = vol.Schema(
    {
        vol.Required(PARAM_SSID): vol.All(str, vol.Length(max=36)),
        vol.Required(PARAM_PASSWORD): vol.All(str, vol.Length(max=64)),
    }
)


class WiFiCommands:
    """Define an object to manage WiFi commands.

    Note that this class shouldn't be instantiated directly; an instance of it will
    automatically be added to the :meth:`Client <aioguardian.Client>` (as
    ``client.wifi``).
    """

    def __init__(self, execute_command: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._execute_command: Callable[..., Coroutine] = execute_command
        self._scan_performed: bool = False

    async def configure(self, ssid: str, password: str, *, silent: bool = True) -> dict:
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

    async def disable_ap(self, *, silent: bool = True) -> dict:
        """Disable the device's onboard WiFi access point.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.wifi_disable_ap, silent=silent)

    async def enable_ap(self, *, silent: bool = True) -> dict:
        """Enable the device's onboard WiFi access point.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.wifi_enable_ap, silent=silent)

    async def list(self, *, silent: bool = True) -> dict:
        """List previously scanned nearby SSIDs.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        if not self._scan_performed:
            _LOGGER.warning(
                "Returning cached SSIDs; run wifi_scan first for up-to-date data"
            )

        list_resp = await self._execute_command(Command.wifi_list, silent=silent)
        self._scan_performed = False
        return list_resp

    async def reset(self, *, silent: bool = True) -> dict:
        """Erase and reset all WiFi settings.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.wifi_reset, silent=silent)

    async def scan(self, *, silent: bool = True) -> dict:
        """Scan for nearby SSIDs.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        scan_resp = await self._execute_command(Command.wifi_scan, silent=silent)
        self._scan_performed = True
        return scan_resp

    async def status(self, *, silent: bool = True) -> dict:
        """Return the current WiFi status of the device.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.wifi_status, silent=silent)
