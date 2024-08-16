"""Test the reset command."""

from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_reset_failure_response.json").encode()]
)
async def test_reset_failure(mock_datagram_client: MagicMock) -> None:
    """Test the wifi_reset command failing.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.wifi.reset()

        assert str(err.value) == (
            "WIFI_RESET command failed (response: {'command': 33, 'status': 'error'})"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_reset_success_response.json").encode()]
)
async def test_reset_success(mock_datagram_client: MagicMock) -> None:
    """Test the wifi_reset command succeeding.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            wifi_reset_response = await client.wifi.reset()

        assert wifi_reset_response["command"] == 33
        assert wifi_reset_response["status"] == "ok"
