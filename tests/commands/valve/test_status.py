"""Test the status command."""

from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_status_failure_response.json").encode()]
)
async def test_status_failure(mock_datagram_client: MagicMock) -> None:
    """Test the valve_status command failing.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.valve.status()

        assert str(err.value) == (
            "VALVE_STATUS command failed (response: {'command': 16, 'status': 'error'})"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_status_success_response.json").encode()]
)
async def test_status_success(mock_datagram_client: MagicMock) -> None:
    """Test the valve_status command succeeding.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            valve_status_response = await client.valve.status()

        assert valve_status_response["command"] == 16
        assert valve_status_response["status"] == "ok"
        assert valve_status_response["data"] == {
            "enabled": False,
            "direction": True,
            "state": "default",
            "travel_count": 0,
            "instantaneous_current": 0,
            "instantaneous_current_ddt": 0,
            "average_current": 34,
        }
