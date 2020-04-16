"""Define a client object to interact with a Guardian device."""
import asyncio
import json
import logging
from typing import Optional

from async_timeout import timeout
import asyncio_dgram

from aioguardian.device import Device
from aioguardian.errors import RequestError, SocketError
from aioguardian.helpers.command import Command

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 7777
DEFAULT_REQUEST_TIMEOUT = 10


class Client:
    """Define the client object.

    :param ip_address: The IP address or FQDN of the Guardian device
    :type ip_address: ``str``
    :param port: The port to connect to
    :type port: ``int``
    :param event_loop: An  ``asyncio`` event loop to attach this Client to
    :type event_loop: ``asyncio.AbstractEventLoop``
    """

    def __init__(
        self,
        ip_address: str,
        *,
        port: int = DEFAULT_PORT,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        """Initialize."""
        self._ip: str = ip_address
        self._loop: Optional[asyncio.AbstractEventLoop] = event_loop
        self._port: int = port
        self._stream: asyncio_dgram.aio.DatagramStream = None

        self.device = Device(self.execute_command)

    async def __aenter__(self):
        """Define an entry point into this object via a context manager."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        """Define an exit point out of this object via a context manager."""
        self.disconnect()

    async def connect(self) -> None:
        """Connect to the Guardian device."""
        async with timeout(DEFAULT_REQUEST_TIMEOUT):
            try:
                self._stream = await asyncio_dgram.connect((self._ip, self._port))
            except asyncio.TimeoutError:
                raise SocketError(f"Connection to device timed out")

    def disconnect(self) -> None:
        """Close the connection."""
        self._stream.close()
        self._stream = None

    async def execute_command(
        self, command: Command, *, params: Optional[dict] = None
    ) -> dict:
        """Make a request against the Guardian device and return the response.

        :param command_integer: The integer denoting the command to execute
        :type url: ``int`` :param params: Any parameters to send along with the command
        :type url: ``dict``
        :rtype: ``dict``
        """
        if not self._stream:
            raise SocketError("You aren't connected to the device yet")

        _params = params or {}
        payload = {"command": command.value, **_params}

        async with timeout(DEFAULT_REQUEST_TIMEOUT):
            try:
                await self._stream.send(json.dumps(payload).encode())
                data, remote_addr = await self._stream.recv()
            except asyncio.TimeoutError:
                raise SocketError(f"{command.name} command timed out")

        decoded_data = json.loads(data.decode())
        _LOGGER.debug("Received data from %s: %s", remote_addr, decoded_data)

        if decoded_data.get("status") != "ok":
            raise RequestError(f"{command.name} command failed: {decoded_data}")

        return decoded_data
