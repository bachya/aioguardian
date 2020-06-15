"""Define a client object to interact with a Guardian device."""
import asyncio
import json
import logging
from types import TracebackType
from typing import Optional, Type

from async_timeout import timeout
import asyncio_dgram

from aioguardian.commands.iot import IOTCommands
from aioguardian.commands.sensor import SensorCommands
from aioguardian.commands.system import SystemCommands
from aioguardian.commands.valve import ValveCommands
from aioguardian.commands.wifi import WiFiCommands
from aioguardian.errors import SocketError, _raise_on_command_error
from aioguardian.helpers.command import Command, get_command_from_code

_LOGGER = logging.getLogger(__name__)

DEFAULT_COMMAND_RETRIES: int = 3
DEFAULT_PORT: int = 7777
DEFAULT_REQUEST_TIMEOUT: int = 10


class Client:  # pylint: disable=too-many-instance-attributes
    """Define the class that can send commands to a Guardian device.

    :param ip_address: The IP address or FQDN of the Guardian device
    :type ip_address: ``str``
    :param port: The port to connect to
    :type port: ``int``
    :param request_timeout: The number of seconds to wait before timing out a request
    :type request_timeout: ``int``
    :param command_retries: The number of attempts to retry a command that times out
    :type command_retries: ``int``
    """

    def __init__(
        self,
        ip_address: str,
        *,
        port: int = DEFAULT_PORT,
        request_timeout: int = DEFAULT_REQUEST_TIMEOUT,
        command_retries: int = DEFAULT_COMMAND_RETRIES,
    ) -> None:
        """Initialize."""
        self._command_retries = command_retries
        self._ip: str = ip_address
        # Since device communication happens over a single UDP port, concurrent
        # operations can return faulty data; we use a lock so the user doesn't have to
        # know anything about that:
        self._lock: asyncio.Lock = asyncio.Lock()
        self._port: int = port
        self._request_timeout: int = request_timeout
        self._stream: asyncio_dgram.aio.DatagramStream = None

        self.iot: IOTCommands = IOTCommands(self._execute_command)
        self.sensor: SensorCommands = SensorCommands(self._execute_command)
        self.system: SystemCommands = SystemCommands(self._execute_command)
        self.valve: ValveCommands = ValveCommands(self._execute_command)
        self.wifi: WiFiCommands = WiFiCommands(self._execute_command)

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

        retry = 0

        while retry < self._command_retries:
            try:
                async with self._lock, timeout(self._request_timeout):
                    await self._stream.send(json.dumps(payload).encode())
                    data, remote_addr = await self._stream.recv()
                    break
            except asyncio.TimeoutError:
                _LOGGER.info("%s command timed out; trying again", command.name)
                retry += 1
                await asyncio.sleep(1)
        else:
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
            raise SocketError("Connection to device timed out")

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
