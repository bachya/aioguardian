"""Define WiFi commands."""
import logging
from typing import Any, Awaitable, Callable, Dict, cast

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

    def __init__(self, execute_command: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._execute_command = execute_command
        self._scan_performed = False

    async def configure(
        self, ssid: str, password: str, *, silent: bool = True
    ) -> Dict[str, Any]:
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

        data = await self._execute_command(
            Command.wifi_configure, params=params, silent=silent
        )
        return cast(Dict[str, Any], data)

    async def disable_ap(self, *, silent: bool = True) -> Dict[str, Any]:
        """Disable the device's onboard WiFi access point.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        data = await self._execute_command(Command.wifi_disable_ap, silent=silent)
        return cast(Dict[str, Any], data)

    async def enable_ap(self, *, silent: bool = True) -> Dict[str, Any]:
        """Enable the device's onboard WiFi access point.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        data = await self._execute_command(Command.wifi_enable_ap, silent=silent)
        return cast(Dict[str, Any], data)

    async def list(self, *, silent: bool = True) -> Dict[str, Any]:
        """List previously scanned nearby SSIDs.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        if not self._scan_performed:
            _LOGGER.warning(
                "Returning cached SSIDs; run wifi_scan first for up-to-date data"
            )

        data = await self._execute_command(Command.wifi_list, silent=silent)
        self._scan_performed = False
        return cast(Dict[str, Any], data)

    async def reset(self, *, silent: bool = True) -> Dict[str, Any]:
        """Erase and reset all WiFi settings.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        data = await self._execute_command(Command.wifi_reset, silent=silent)
        return cast(Dict[str, Any], data)

    async def scan(self, *, silent: bool = True) -> Dict[str, Any]:
        """Scan for nearby SSIDs.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        data = await self._execute_command(Command.wifi_scan, silent=silent)
        self._scan_performed = True
        return cast(Dict[str, Any], data)

    async def status(self, *, silent: bool = True) -> Dict[str, Any]:
        """Return the current WiFi status of the device.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        data = await self._execute_command(Command.wifi_status, silent=silent)
        return cast(Dict[str, Any], data)
