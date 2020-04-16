"""Test the wifi_reset command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_reset_failure_response.json").encode()]
)
async def test_wifi_reset_failure(mock_datagram_client):
    """Test the wifi_reset command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.device.wifi_reset()

    assert str(err.value) == (
        "wifi_reset command failed (response: {'command': 33, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_reset_success_response.json").encode()]
)
async def test_wifi_reset_success(mock_datagram_client):
    """Test the wifi_reset command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            wifi_reset_response = await client.device.wifi_reset()
        assert wifi_reset_response["command"] == 33
        assert wifi_reset_response["status"] == "ok"
