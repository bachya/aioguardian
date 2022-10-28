"""Test the list command."""
from unittest.mock import MagicMock, Mock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_list_failure_response.json").encode()]
)
async def test_list_failure(mock_datagram_client: MagicMock) -> None:
    """Test the wifi_list command failing.

    Args:
        mock_datagram_client: A mocked UDP client.
    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.wifi.list()

        assert str(err.value) == (
            "WIFI_LIST command failed (response: {'command': 38, 'status': 'error'})"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_list_success_response.json").encode()]
)
async def test_list_success(caplog: Mock, mock_datagram_client: MagicMock) -> None:
    """Test the wifi_list command succeeding.

    Args:
        caplog: A mocked logging facility.
        mock_datagram_client: A mocked UDP client.
    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            await client.wifi.scan()
            wifi_list_response = await client.wifi.list()

        assert all(
            "Returning cached SSIDs; run wifi_scan first for up-to-date data"
            not in e.message
            for e in caplog.records
        )

        assert wifi_list_response["command"] == 38
        assert wifi_list_response["status"] == "ok"
        assert wifi_list_response["data"] == {
            "record_count": 1,
            "records": [
                {
                    "bssid": "60:31:97:BE:53:5D",
                    "rssi": -89,
                    "channel": 1,
                    "authmode": 4,
                    "ssid": "CenturyLink0526",
                }
            ],
        }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_list_success_response.json").encode()]
)
async def test_list_success_cached(
    caplog: Mock, mock_datagram_client: MagicMock
) -> None:
    """Test the wifi_list command succeeding after a cache.

    Args:
        caplog: A mocked logging facility.
        mock_datagram_client: A mocked UDP client.
    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            wifi_list_response = await client.wifi.list()

        assert any(
            "Returning cached SSIDs; run wifi_scan first for up-to-date data"
            in e.message
            for e in caplog.records
        )

        assert wifi_list_response["command"] == 38
        assert wifi_list_response["status"] == "ok"
        assert wifi_list_response["data"] == {
            "record_count": 1,
            "records": [
                {
                    "bssid": "60:31:97:BE:53:5D",
                    "rssi": -89,
                    "channel": 1,
                    "authmode": 4,
                    "ssid": "CenturyLink0526",
                }
            ],
        }
