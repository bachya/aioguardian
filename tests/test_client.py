"""Test generic client characteristics."""
import asyncio

from asynctest import CoroutineMock, patch
import pytest

from aioguardian import Client
from aioguardian.errors import SocketError


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
