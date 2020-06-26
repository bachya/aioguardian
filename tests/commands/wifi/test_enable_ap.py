"""Test the enable_ap command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_enable_ap_failure_response.json").encode()]
)
async def test_enable_ap_failure(mock_datagram_client):
    """Test the wifi_enable_ap command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.wifi.enable_ap()

        assert str(err.value) == (
            "wifi_enable_ap command failed "
            "(response: {'command': 35, 'status': 'error'})"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_enable_ap_success_response.json").encode()]
)
async def test_enable_ap_success(mock_datagram_client):
    """Test the wifi_enable_ap command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            wifi_enable_ap_response = await client.wifi.enable_ap()

        assert wifi_enable_ap_response["command"] == 35
        assert wifi_enable_ap_response["status"] == "ok"
