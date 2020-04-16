"""Test the valve_status command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_status_failure_response.json").encode()]
)
async def test_valve_status_failure(mock_datagram_client):
    """Test the valve_status command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.valve.valve_status()

    assert str(err.value) == (
        "valve_status command failed (response: {'command': 16, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_status_success_response.json").encode()]
)
async def test_valve_status_success(mock_datagram_client):
    """Test the valve_status command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            valve_status_response = await client.valve.valve_status()
        assert valve_status_response["command"] == 16
        assert valve_status_response["status"] == "ok"
        valve_status_response["data"]["enabled"] = False
        valve_status_response["data"]["direction"] = True
        valve_status_response["data"]["state"] = "default"
        valve_status_response["data"]["travel_count"] = 0
        valve_status_response["data"]["instantaneous_current"] = 0
        valve_status_response["data"]["instantaneous_current_ddt"] = 0
        valve_status_response["data"]["average_current"] = 34
