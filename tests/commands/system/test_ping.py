"""Test the ping command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_failure_response.json").encode()]
)
async def test_ping_failure(mock_datagram_client):
    """Test a failured ping of the device."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.system.ping()

    assert str(err.value) == (
        "ping command failed (response: {'command': 0, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_success_response.json").encode()]
)
async def test_ping_success(mock_datagram_client):
    """Test the ping command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            ping_response = await client.system.ping()

        assert ping_response["command"] == 0
        assert ping_response["status"] == "ok"
        assert ping_response["data"]["uid"] == "ABCDEF123456"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_success_silent_response.json").encode()]
)
async def test_ping_silent_success(mock_datagram_client):
    """Test the ping command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            ping_response = await client.system.ping()

        assert ping_response["command"] == 0
        assert ping_response["status"] == "ok"
        assert ping_response["silent"] is True
        assert ping_response["data"]["uid"] == "ABCDEF123456"
