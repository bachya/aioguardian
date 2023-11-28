"""Define a client object to interact with a Guardian device."""
from __future__ import annotations

import asyncio
import json
from types import TracebackType
from typing import Any, cast

import asyncio_dgram

from aioguardian.commands.iot import IOTCommands
from aioguardian.commands.sensor import SensorCommands
from aioguardian.commands.system import SystemCommands
from aioguardian.commands.valve import ValveCommands
from aioguardian.commands.wifi import WiFiCommands
from aioguardian.const import LOGGER
from aioguardian.errors import SocketError, _raise_on_command_error
from aioguardian.helpers.command import Command, get_command_from_code

DEFAULT_COMMAND_RETRIES: int = 3
DEFAULT_PORT: int = 7777
DEFAULT_REQUEST_TIMEOUT: int = 10

try:
    timeout_callable = asyncio.timeout  # type: ignore[attr-defined]
except AttributeError:  # pragma: no cover
    import async_timeout  # pylint: disable=import-error

    timeout_callable = async_timeout.timeout


class Client:  # pylint: disable=too-many-instance-attributes
    """Define the class that can send commands to a Guardian device.

    Args:
        ip_address: The IP address or hostname of a Guardian valve controller.
        port: The port to connect to.
        request_timeout: The number of seconds to wait before timing out a request.
        command_retries: The number of retries to use on a failed command.
    """

    def __init__(
        self,
        ip_address: str,
        *,
        port: int = DEFAULT_PORT,
        request_timeout: int = DEFAULT_REQUEST_TIMEOUT,
        command_retries: int = DEFAULT_COMMAND_RETRIES,
    ) -> None:
        """Initialize.

        Args:
            ip_address: The IP address or hostname of a Guardian valve controller.
            port: The port to connect to.
            request_timeout: The number of seconds to wait before timing out a request.
            command_retries: The number of retries to use on a failed command.
        """
        self._command_retries = command_retries
        self._ip = ip_address
        # Since device communication happens over a single UDP port, concurrent
        # operations can return faulty data; we use a lock so the user doesn't have to
        # know anything about that:
        self._lock: asyncio.Lock = asyncio.Lock()
        self._port = port
        self._request_timeout = request_timeout
        self._stream: asyncio_dgram.aio.DatagramStream | None = None

        self.iot = IOTCommands(self._execute_command)
        self.sensor = SensorCommands(self._execute_command)
        self.system = SystemCommands(self._execute_command)
        self.valve = ValveCommands(self._execute_command)
        self.wifi = WiFiCommands(self._execute_command)

    async def __aenter__(self) -> Client:
        """Define an entry point into this object via a context manager.

        Returns:
            A connected aioguardian client.
        """
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,  # noqa: F841
        exc_val: BaseException | None,  # noqa: F841
        exc_tb: TracebackType | None,  # noqa: F841
    ) -> None:
        """Define an exit point out of this object via a context manager.

        Args:
            exc_type: An optional exception if one caused the context manager to close.
            exc_val: The value of the optional exception
            exc_tb: The traceback of the optional exception
        """
        self.disconnect()

    async def _execute_command(
        self, command: Command, *, params: dict | None = None, silent: bool = True
    ) -> dict[str, Any]:
        """Make a request against the Guardian device and return the response.

        Args:
            command: The command to execute.
            params: Any parameters to send along with the command.
            silent: If ``True``, silence "beep" tones associated with this command.

        Returns:
            An API response payload.

        Raises:
            SocketError: Raised on an issue with the UDP socket.
        """
        if not self._stream:
            raise SocketError("You aren't connected to the device yet")

        _params = params or {}
        payload = {"command": command.value, "silent": silent, **_params}

        retry = 0

        while retry < self._command_retries:
            try:
                async with self._lock, timeout_callable(self._request_timeout):
                    await self._stream.send(  # type: ignore[attr-defined]
                        json.dumps(payload).encode()
                    )
                    data, remote_addr = await self._stream.recv()
                    break
            except asyncio.TimeoutError:
                LOGGER.info("%s command timed out; trying again", command.name)
                retry += 1
                await asyncio.sleep(1)
        else:
            raise SocketError(f"{command.name} command timed out")

        decoded_data = json.loads(data.decode())
        LOGGER.debug("Received data from %s: %s", remote_addr, decoded_data)

        _raise_on_command_error(command, decoded_data)

        return cast(dict[str, Any], decoded_data)

    async def connect(self) -> None:
        """Connect to the Guardian device.

        Raises:
            SocketError: Raised on an issue with the UDP socket.
        """
        try:
            async with timeout_callable(self._request_timeout):
                self._stream = await asyncio_dgram.connect((self._ip, self._port))
        except asyncio.TimeoutError:
            raise SocketError("Connection to device timed out") from None

    def disconnect(self) -> None:
        """Close the connection."""
        if self._stream:
            self._stream.close()
            self._stream = None

    async def execute_raw_command(
        self, command_code: int, *, params: dict | None = None, silent: bool = True
    ) -> dict[str, Any]:
        """Execute a command via its integer-based command code.

        Args:
            command_code: The command code to execute.
            params: Any parameters to send along with the command.
            silent: If ``True``, silence "beep" tones associated with this command.

        Returns:
            An API response payload.
        """
        command = get_command_from_code(command_code)
        return await self._execute_command(command, params=params, silent=silent)
