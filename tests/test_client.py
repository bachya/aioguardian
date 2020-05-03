"""Test generic client characteristics."""
import asyncio

from asynctest import CoroutineMock, patch
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError, SocketError

from tests.common import load_fixture


@pytest.mark.asyncio
async def test_command_without_socket_connect():
    """Test that executing a command without an open connection throws an exception."""
    client = Client("192.168.1.100")
    with pytest.raises(SocketError) as err:
        await client.device.ping()

    assert str(err.value) == "You aren't connected to the device yet"


@pytest.mark.asyncio
async def test_connect_timeout():
    """Test that a timeout during connection throws an exception."""
    with patch(
        "asyncio_dgram.connect", CoroutineMock(side_effect=asyncio.TimeoutError)
    ):
        with pytest.raises(SocketError) as err:
            async with Client("192.168.1.100") as client:
                await client.device.ping()

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


@pytest.mark.asyncio
async def test_request_timeout():
    """Test that a timeout during command execution throws an exception."""
    with patch(
        "asyncio_dgram.aio.DatagramStream.send",
        CoroutineMock(side_effect=asyncio.TimeoutError),
    ):
        with pytest.raises(SocketError) as err:
            async with Client("192.168.1.100") as client:
                await client.device.ping()

        assert str(err.value) == "ping command timed out"


@pytest.mark.asyncio
async def test_unknown_command():
    """Test that an unknown command throws an exception."""
    with patch(
        "asyncio_dgram.aio.DatagramStream.send",
        CoroutineMock(side_effect=asyncio.TimeoutError),
    ):
        with pytest.raises(SocketError) as err:
            async with Client("192.168.1.100") as client:
                await client.device.ping()

        assert str(err.value) == "ping command timed out"


@pytest.mark.asyncio
async def test_unknown_raw_command(mock_datagram_client):
    """Test that an unknown raw command throws an exception."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                await client.execute_raw_command(999)

        assert str(err.value) == "Unknown command code: 999"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_success_response.json").encode()]
)
async def test_wrong_response(mock_datagram_client):
    """Test the case when the device returns a response other than the command."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                await client.device.wifi_status()

        assert (
            str(err.value)
            == "Sent command wifi_status, but got response for command ping"
        )
