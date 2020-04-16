"""Test the sensor_status command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("sensor_status_success_response.json").encode()]
)
async def test_sensor_status_success(mock_datagram_client):
    """Test the sensor_status command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            sensor_status_response = await client.sensor.sensor_status()
        assert sensor_status_response["command"] == 80
        assert sensor_status_response["status"] == "ok"
        assert sensor_status_response["data"]["temperature"] == 71
        assert sensor_status_response["data"]["wet"] is False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("sensor_status_failure_response.json").encode()]
)
async def test_sensor_status_failure(mock_datagram_client):
    """Test the sensor_status command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.sensor.sensor_status()

    assert str(err.value) == (
        "sensor_status command failed (response: {'command': 80, 'status': 'error'})"
    )
