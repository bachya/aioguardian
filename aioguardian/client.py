"""Define a client object to interact with a Guardian device."""
import asyncio
import json
import logging
from typing import Optional

from async_timeout import timeout
import asyncio_dgram

from aioguardian.commands.device import Device
from aioguardian.commands.sensor import Sensor
from aioguardian.commands.valve import Valve
from aioguardian.errors import SocketError, _raise_on_command_error
from aioguardian.helpers.command import Command

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT: int = 7777
DEFAULT_REQUEST_TIMEOUT: int = 10


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
        self, exc_type: Exception, exc_value: str, traceback: str
    ) -> None:
        """Define an exit point out of this object via a context manager."""
        self.disconnect()

    async def _execute_command(
        self, command: Command, *, params: Optional[dict] = None
    ) -> dict:
        """Make a request against the Guardian device and return the response.

        :param command: The command to run
        :type command: :meth:`aioguardian.helpers.command.Command`
        :param params: Any parameters to send along with the command
        :type params: ``dict``
        :rtype: ``dict``
        """
        if not self._stream:
            raise SocketError("You aren't connected to the device yet")

        _params = params or {}
        payload = {"command": command.value, **_params}

        async with timeout(self._request_timeout):
            try:
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
        async with timeout(self._request_timeout):
            try:
                self._stream = await asyncio_dgram.connect((self._ip, self._port))
            except asyncio.TimeoutError:
                raise SocketError(f"Connection to device timed out")

    def disconnect(self) -> None:
        """Close the connection."""
        self._stream.close()
        self._stream = None
