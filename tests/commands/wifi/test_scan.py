"""Test the scan command."""

from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_scan_failure_response.json").encode()]
)
async def test_scan_failure(mock_datagram_client: MagicMock) -> None:
    """Test the wifi_scan command failing.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.wifi.scan()

        assert str(err.value) == (
            "WIFI_SCAN command failed (response: {'command': 37, 'status': 'error'})"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_scan_success_response.json").encode()]
)
async def test_scan_success(mock_datagram_client: MagicMock) -> None:
    """Test the wifi_scan command succeeding.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            wifi_scan_response = await client.wifi.scan()

        assert wifi_scan_response["command"] == 37
        assert wifi_scan_response["status"] == "ok"
