"""Test the disable_ap command."""

from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_disable_ap_failure_response.json").encode()]
)
async def test_disable_ap_failure(mock_datagram_client: MagicMock) -> None:
    """Test the wifi_disable_ap command failing.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.wifi.disable_ap()

        assert str(err.value) == (
            "WIFI_DISABLE_AP command failed "
            "(response: {'command': 36, 'status': 'error'})"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_disable_ap_success_response.json").encode()]
)
async def test_disable_ap_success(mock_datagram_client: MagicMock) -> None:
    """Test the wifi_disable_ap command succeeding.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            wifi_disable_ap_response = await client.wifi.disable_ap()

        assert wifi_disable_ap_response["command"] == 36
        assert wifi_disable_ap_response["status"] == "ok"
