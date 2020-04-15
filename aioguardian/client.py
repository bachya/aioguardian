"""Define a client object to interact with a Guardian device."""
import asyncio
import json
import logging
from typing import Optional, Union

from async_timeout import timeout
import asyncio_dgram

from .device import Device
from .errors import RequestError, SocketError

_LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 7777
DEFAULT_REQUEST_TIMEOUT = 10


def _get_event_loop() -> asyncio.AbstractEventLoop:
    """Retrieve the event loop or creates a new one."""
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


class Client:  # pylint: disable=too-few-public-methods
    """Define the client object.

    :param ip_address: The IP address or FQDN of the Guardian device
    :type ip_address: ``str``
    :param port: The port to connect to
    :type port: ``int``
    :param use_async: Whether to use async mode
    :type use_async: ``bool``
    :param event_loop: An  ``asyncio`` event loop to attach this Client to
    :type event_loop: ``asyncio.AbstractEventLoop``
    """

    def __init__(
        self,
        ip_address: str,
        *,
        port: int = DEFAULT_PORT,
        use_async: bool = False,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
        """Initialize."""
        self._ip = ip_address
        self._loop = event_loop
        self._port = port
        self._use_async = use_async

        self.device = Device(self.execute_command)

    def execute_command(
        self, command_integer: int, *, params: Optional[dict] = None
    ) -> Union[dict, asyncio.Future]:
        """Make a request against the Guardian device and return the response.

        :param command_integer: The integer denoting the command to execute
        :type url: ``int``
        :param params: Any parameters to send along with the command
        :type url: ``dict``
        :rtype: ``dict``
        """
        _params = params or {}
        payload = {"command": command_integer, **_params}

        async def request():
            async with timeout(DEFAULT_REQUEST_TIMEOUT):
                try:
                    stream = await asyncio_dgram.connect((self._ip, self._port))
                    await stream.send(json.dumps(payload).encode())
                    data, remote_addr = await stream.recv()
                    stream.close()
                except (asyncio.CancelledError, asyncio.TimeoutError):
                    raise SocketError(f"Request timed out (command: {command_integer})")

            decoded_data = json.loads(data.decode())
            _LOGGER.debug("Received data from %s: %s", remote_addr, decoded_data)

            if decoded_data.get("status") != "ok":
                raise RequestError(f"The API call failed: {decoded_data}")

            return decoded_data

        if not self._loop:
            self._loop = _get_event_loop()

        future = asyncio.ensure_future(request(), loop=self._loop)

        if self._use_async:
            return future
        return self._loop.run_until_complete(future)
