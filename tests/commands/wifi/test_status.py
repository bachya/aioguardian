"""Test the status command."""

from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_status_failure_response.json").encode()]
)
async def test_status_failure(mock_datagram_client: MagicMock) -> None:
    """Test the wifi_status command failing.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.wifi.status()

        assert str(err.value) == (
            "WIFI_STATUS command failed (response: {'command': 32, 'status': 'error'})"
        )


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_status_success_response.json").encode()]
)
async def test_status_success(mock_datagram_client: MagicMock) -> None:
    """Test the wifi_status command succeeding.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            wifi_status_response = await client.wifi.status()

        assert wifi_status_response["command"] == 32
        assert wifi_status_response["status"] == "ok"
        assert wifi_status_response["data"] == {
            "station_connected": True,
            "ip_assigned": True,
            "mqtt_connected": True,
            "rssi": -63,
            "channel": 1,
            "lan_ipv4": "192.168.1.100",
            "lan_ipv6": "AC10:BD0:FFFF:FFFF:AC10:BD0:FFFF:FFFF",
            "ap_enabled": True,
            "ap_clients": 0,
            "bssid": "ABCDEF123456",
            "ssid": "My_Network",
        }
