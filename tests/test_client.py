"""Test generic client characteristics."""
import asyncio

from asynctest import CoroutineMock, patch
import pytest

from aioguardian import Client
from aioguardian.client import _get_event_loop
from aioguardian.errors import SocketError


def test_get_event_loop():
    """Test getting the active (or a new) event loop."""
    loop = _get_event_loop()  # pylint: disable=protected-access
    assert isinstance(loop, asyncio.AbstractEventLoop)

    # Test there being no currently running event loop generates one:
    with patch("asyncio.get_event_loop", side_effect=RuntimeError):
        loop = _get_event_loop()  # pylint: disable=protected-access
        assert isinstance(loop, asyncio.AbstractEventLoop)


@pytest.mark.asyncio
async def test_request_timeout():
    """Test a successful ping of the device in async mode."""
    client = Client("192.168.1.100", use_async=True)

    with patch(
        "asyncio_dgram.connect", CoroutineMock(side_effect=asyncio.TimeoutError)
    ):
        with pytest.raises(SocketError) as err:
            await client.device.ping()
            assert "Request timed out" in err
