"""Test the valve_open command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_open_failure_response.json").encode()]
)
async def test_valve_open_failure(mock_datagram_client):
    """Test the valve_open command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.valve.valve_open()

    assert str(err.value) == "valve_open command failed: valve_moving"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_open_success_response.json").encode()]
)
async def test_valve_open_success(mock_datagram_client):
    """Test the valve_open command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            valve_open_response = await client.valve.valve_open()

        assert valve_open_response["command"] == 17
