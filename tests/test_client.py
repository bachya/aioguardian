"""Test generic client characteristics."""
import asyncio

import pytest

from aioguardian import Client
from aioguardian.errors import SocketError

from tests.async_mock import AsyncMock, patch
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize("recv_response", [AsyncMock(side_effect=asyncio.TimeoutError)])
async def test_command_timeout(mock_datagram_client):
    """Test that a timeout during command execution throws an exception."""
    with mock_datagram_client, patch("asyncio.sleep"):
        with pytest.raises(SocketError) as err:
            async with Client("192.168.1.100") as client:
                await client.system.ping()

        assert str(err.value) == "system_ping command timed out"


@pytest.mark.asyncio
async def test_command_timeout_successful_retry(mock_datagram_client):
    """Test that a timeout during command execution throws an exception."""
    with mock_datagram_client, patch("asyncio.sleep"):
        mock_datagram_client.recv.side_effect = [
            asyncio.TimeoutError,
            (load_fixture("ping_success_response.json").encode(), "192.168.1.100"),
        ]

        async with Client("192.168.1.100") as client:
            ping_response = await client.system.ping()

        assert ping_response["command"] == 0
        assert ping_response["status"] == "ok"
        assert ping_response["data"]["uid"] == "ABCDEF123456"


@pytest.mark.asyncio
async def test_command_without_socket_connect():
    """Test that executing a command without an open connection throws an exception."""
    client = Client("192.168.1.100")
    with pytest.raises(SocketError) as err:
        await client.system.ping()

    assert str(err.value) == "You aren't connected to the device yet"


@pytest.mark.asyncio
async def test_connect_timeout():
    """Test that a timeout during connection throws an exception."""
    with patch("asyncio_dgram.connect", AsyncMock(side_effect=asyncio.TimeoutError)):
        with pytest.raises(SocketError) as err:
            async with Client("192.168.1.100") as client:
                await client.system.ping()

        assert str(err.value) == "Connection to device timed out"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_success_response.json").encode()]
)
async def test_raw_command_success(mock_datagram_client):
    """Test a successful raw command."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            ping_response = await client.execute_raw_command(0)

        assert ping_response["command"] == 0
        assert ping_response["status"] == "ok"
        assert ping_response["data"]["uid"] == "ABCDEF123456"
