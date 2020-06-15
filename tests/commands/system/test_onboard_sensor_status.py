"""Test the onboard_sensor_status command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("onboard_sensor_status_success_response.json").encode()],
)
async def test_onboard_sensor_status_success(mock_datagram_client):
    """Test the onboard_sensor_status command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            onboard_sensor_status = await client.system.onboard_sensor_status()

        assert onboard_sensor_status["command"] == 80
        assert onboard_sensor_status["status"] == "ok"
        assert onboard_sensor_status["data"]["temperature"] == 71
        assert onboard_sensor_status["data"]["wet"] is False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("onboard_sensor_status_failure_response.json").encode()],
)
async def test_onboard_sensor_status_failure(mock_datagram_client):
    """Test the onboard_sensor_status command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.system.onboard_sensor_status()

    assert str(err.value) == (
        "system_onboard_sensor_status command failed "
        "(response: {'command': 80, 'status': 'error'})"
    )
