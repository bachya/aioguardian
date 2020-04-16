"""Test generic client characteristics."""
import asyncio

from asynctest import CoroutineMock, patch
import pytest

from aioguardian import Client
from aioguardian.errors import SocketError


@pytest.mark.asyncio
async def test_command_without_socket_connect():
    """Test that executing a command without an open connection throws an exception."""
    client = Client("192.168.1.100")
    with pytest.raises(SocketError) as err:
        await client.device.ping()
        assert "You aren't connected to the device yet" in err


@pytest.mark.asyncio
async def test_connect_timeout():
    """Test that a timeout during connection throws an exception."""
    with patch(
        "asyncio_dgram.connect", CoroutineMock(side_effect=asyncio.TimeoutError)
    ):
        with pytest.raises(SocketError) as err:
            async with Client("192.168.1.100") as client:
                await client.device.ping()
            assert "Connection to device timed out" in err


@pytest.mark.asyncio
async def test_request_timeout():
    """Test that a timeout during connection throws an exception."""
    with patch(
        "asyncio_dgram.aio.DatagramStream.send",
        CoroutineMock(side_effect=asyncio.TimeoutError),
    ):
        with pytest.raises(SocketError) as err:
            async with Client("192.168.1.100") as client:
                await client.device.ping()
            assert "Request timed out" in err
