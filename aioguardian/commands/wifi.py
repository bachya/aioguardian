"""Define WiFi commands."""
import logging
from collections.abc import Awaitable, Callable
from typing import Any, cast

import voluptuous as vol

from aioguardian.errors import CommandError
from aioguardian.helpers.command import Command

_LOGGER = logging.getLogger(__name__)

PARAM_PASSWORD = "password"  # noqa: S105, # nosec
PARAM_SSID = "ssid"

WIFI_CONFIGURE_PARAM_SCHEMA = vol.Schema(
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

    Args:
        execute_command: The execute_command method from the Client object.
    """

    def __init__(self, execute_command: Callable[..., Awaitable]) -> None:
        """Initialize.

        Args:
            execute_command: The execute_command method from the Client object.
        """
        self._execute_command = execute_command
        self._scan_performed = False

    async def configure(
        self, ssid: str, password: str, *, silent: bool = True
    ) -> dict[str, Any]:
        """Configure the device to use a wireless network.

        Args:
            ssid: An SSID to connect to.
            password: The password to use to connect to the SSID.
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.

        Raises:
            CommandError: Raised when invalid parameters are provided.
        """
        params = {PARAM_SSID: ssid, PARAM_PASSWORD: password}

        try:
            WIFI_CONFIGURE_PARAM_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        data = await self._execute_command(
            Command.WIFI_CONFIGURE, params=params, silent=silent
        )
        return cast(dict[str, Any], data)

    async def disable_ap(self, *, silent: bool = True) -> dict[str, Any]:
        """Disable the device's onboard WiFi access point.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        data = await self._execute_command(Command.WIFI_DISABLE_AP, silent=silent)
        return cast(dict[str, Any], data)

    async def enable_ap(self, *, silent: bool = True) -> dict[str, Any]:
        """Enable the device's onboard WiFi access point.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        data = await self._execute_command(Command.WIFI_ENABLE_AP, silent=silent)
        return cast(dict[str, Any], data)

    async def list(self, *, silent: bool = True) -> dict[str, Any]:
        """List previously scanned nearby SSIDs.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        if not self._scan_performed:
            _LOGGER.warning(
                "Returning cached SSIDs; run wifi_scan first for up-to-date data"
            )

        data = await self._execute_command(Command.WIFI_LIST, silent=silent)
        self._scan_performed = False
        return cast(dict[str, Any], data)

    async def reset(self, *, silent: bool = True) -> dict[str, Any]:
        """Erase and reset all WiFi settings.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        data = await self._execute_command(Command.WIFI_RESET, silent=silent)
        return cast(dict[str, Any], data)

    async def scan(self, *, silent: bool = True) -> dict[str, Any]:
        """Scan for nearby SSIDs.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        data = await self._execute_command(Command.WIFI_SCAN, silent=silent)
        self._scan_performed = True
        return cast(dict[str, Any], data)

    async def status(self, *, silent: bool = True) -> dict[str, Any]:
        """Return the current WiFi status of the device.

        Args:
            silent: Whether the valve controller should beep upon successful command.

        Returns:
            An API response payload.
        """
        data = await self._execute_command(Command.WIFI_STATUS, silent=silent)
        return cast(dict[str, Any], data)
