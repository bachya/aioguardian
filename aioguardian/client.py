"""Define a client object to interact with a Guardian device."""
import asyncio
import json
import logging
from types import TracebackType
from typing import Optional, Type

from async_timeout import timeout
import asyncio_dgram

from aioguardian.commands.device import Device
from aioguardian.commands.sensor import Sensor
from aioguardian.commands.valve import Valve
from aioguardian.errors import ERROR_CODE_MAPPING, CommandError, SocketError
from aioguardian.helpers.command import Command, get_command_from_code

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT: int = 7777
DEFAULT_REQUEST_TIMEOUT: int = 10


def _raise_on_command_error(command: Command, data: dict) -> None:
    """Examine a data response and raise errors appropriately.

    :param command: The command that was run
    :type command: :meth:`aioguardian.helpers.command.Command`
    :param data: The response data from running the command
    :type params: ``dict``
    """
    # The device API has a bug where it can sporadically return data for a command other
    # than the one that was submitted; if we detect this, raise:
    if data["command"] != command.value:
        received_command = get_command_from_code(data["command"])
        raise CommandError(
            f"Sent {command.name} command, but got response for "
            f"{received_command.name} command"
        )

    # If we're okay, we're okay:
    if data.get("status") == "ok":
        return

    # If we know exactly why the command failed, raise that error:
    if data.get("error_code") in ERROR_CODE_MAPPING:
        raise CommandError(
            f"{command.name} command failed: {ERROR_CODE_MAPPING[data['error_code']]}"
        )

    # Last resort, return a generic error with the response payload:
    raise CommandError(f"{command.name} command failed (response: {data})")


class Client:
    """Define the class that can send commands to a Guardian device.

    :param ip_address: The IP address or FQDN of the Guardian device
    :type ip_address: ``str``
    :param port: The port to connect to
    :type port: ``int``
    :param request_timeout: The number of seconds to wait before timing out a request
    :type request_timeout: ``int``
    """

    def __init__(
        self,
        ip_address: str,
        *,
        port: int = DEFAULT_PORT,
        request_timeout: int = DEFAULT_REQUEST_TIMEOUT,
    ) -> None:
        """Initialize."""
        self._ip: str = ip_address
        self._port: int = port
        self._request_timeout: int = request_timeout
        self._stream: asyncio_dgram.aio.DatagramStream = None

        self.device: Device = Device(self._execute_command)
        self.sensor: Sensor = Sensor(self._execute_command)
        self.valve: Valve = Valve(self._execute_command)

    async def __aenter__(self) -> "Client":
        """Define an entry point into this object via a context manager."""
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """Define an exit point out of this object via a context manager."""
        self.disconnect()

    async def _execute_command(
        self, command: Command, *, params: Optional[dict] = None, silent: bool = True
    ) -> dict:
        """Make a request against the Guardian device and return the response.

        :param command: The command to execute
        :type command: :meth:`aioguardian.helpers.command.Command`
        :param params: Any parameters to send along with the command
        :type params: ``dict``
        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        if not self._stream:
            raise SocketError("You aren't connected to the device yet")

        _params = params or {}
        payload = {"command": command.value, "silent": silent, **_params}

        try:
            async with timeout(self._request_timeout):
                await self._stream.send(json.dumps(payload).encode())
                data, remote_addr = await self._stream.recv()
        except asyncio.TimeoutError:
            raise SocketError(f"{command.name} command timed out")

        decoded_data = json.loads(data.decode())
        _LOGGER.debug("Received data from %s: %s", remote_addr, decoded_data)

        _raise_on_command_error(command, decoded_data)

        return decoded_data

    async def connect(self) -> None:
        """Connect to the Guardian device."""
        try:
            async with timeout(self._request_timeout):
                self._stream = await asyncio_dgram.connect((self._ip, self._port))
        except asyncio.TimeoutError:
            raise SocketError(f"Connection to device timed out")

    def disconnect(self) -> None:
        """Close the connection."""
        self._stream.close()
        self._stream = None

    async def execute_raw_command(
        self, command_code: int, *, params: Optional[dict] = None, silent: bool = True
    ) -> dict:
        """Execute a command via its integer-based command code.

        A mapping of command-code-to-command can be seen in the
        :meth:`Command <aioguardian.helpers.command.Command>` helper.

        :param command: The command code to execute
        :type command: ``int``
        :param params: Any parameters to send along with the command
        :type params: ``dict``
        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        command = get_command_from_code(command_code)
        return await self._execute_command(command, params=params, silent=silent)
