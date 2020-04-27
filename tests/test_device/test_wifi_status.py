"""Test the wifi_status command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_status_failure_response.json").encode()]
)
async def test_wifi_status_failure(mock_datagram_client):
    """Test the wifi_status command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.device.wifi_status()

    assert str(err.value) == (
        "wifi_status command failed (response: {'command': 32, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_status_success_response.json").encode()]
)
async def test_wifi_status_success(mock_datagram_client):
    """Test the wifi_status command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            wifi_status_response = await client.device.wifi_status()

        assert wifi_status_response["command"] == 32
        assert wifi_status_response["status"] == "ok"
        assert wifi_status_response["data"]["station_connected"] is True
        assert wifi_status_response["data"]["ip_assigned"] is True
        assert wifi_status_response["data"]["mqtt_connected"] is True
        assert wifi_status_response["data"]["rssi"] == -63
        assert wifi_status_response["data"]["channel"] == 1
        assert wifi_status_response["data"]["lan_ipv4"] == "192.168.1.100"
        assert (
            wifi_status_response["data"]["lan_ipv6"]
            == "AC10:BD0:FFFF:FFFF:AC10:BD0:FFFF:FFFF"
        )
        assert wifi_status_response["data"]["ap_enabled"] is True
        assert wifi_status_response["data"]["ap_clients"] == 0
        assert wifi_status_response["data"]["bssid"] == "ABCDEF123456"
        assert wifi_status_response["data"]["ssid"] == "My_Network"
