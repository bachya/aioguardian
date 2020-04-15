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
    """Define the client object."""

    def __init__(
        self,
        ip_address: str,
        *,
        port: int = DEFAULT_PORT,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
        use_async: bool = False,
    ):
        """Initialize."""
        self._ip = ip_address
        self._loop = event_loop
        self._port = port
        self._use_async = use_async

        self.device = Device(self.execute_command)

    def execute_command(
        self, command_decimal: int, *, params: Optional[dict] = None
    ) -> Union[dict, asyncio.Future]:
        """Make a request against the Guardian device and return the response."""
        _params = params or {}
        payload = {"command": command_decimal, **_params}

        async def request():
            async with timeout(DEFAULT_REQUEST_TIMEOUT):
                try:
                    stream = await asyncio_dgram.connect((self._ip, self._port))
                    await stream.send(json.dumps(payload).encode())
                    data, remote_addr = await stream.recv()
                    stream.close()
                except (asyncio.CancelledError, asyncio.TimeoutError):
                    raise SocketError(f"Request timed out (command: {command_decimal})")

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
