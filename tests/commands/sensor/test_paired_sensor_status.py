"""Test the paired_sensor_status command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("paired_sensor_status_failure_3_response.json").encode()],
)
async def test_paired_sensor_status_failure_not_paired(mock_datagram_client):
    """Test the paired_sensor_status command failing because it isn't paired."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.sensor.paired_sensor_status("ABCDE1234567")

        assert (
            str(err.value)
            == "sensor_paired_sensor_status command failed: sensor_not_paired"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("paired_sensor_status_failure_5_response.json").encode()],
)
async def test_paired_sensor_status_failure_error_loading(mock_datagram_client):
    """Test the paired_sensor_status command failing because of a loading error."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.sensor.paired_sensor_status("ABCDE1234567")

        assert (
            str(err.value)
            == "sensor_paired_sensor_status command failed: sensor_error_loading"
        )


@pytest.mark.asyncio
async def test_paired_sensor_status_invalid_uid(mock_datagram_client):
    """Test that an invalid UID throws an exception."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.sensor.paired_sensor_status("$@&*!@--")

        assert str(err.value) == (
            "Invalid parameters provided: String is not alphanumeric for dictionary "
            "value @ data['uid']"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("paired_sensor_status_success_response.json").encode()],
)
async def test_paired_sensor_status_dump_success(mock_datagram_client):
    """Test the pair_dump command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            paired_sensor_status = await client.sensor.paired_sensor_status(
                "ABCDE1234567"
            )

        assert paired_sensor_status["command"] == 51
        assert paired_sensor_status["status"] == "ok"
        assert paired_sensor_status["data"] == {
            "uid": "6309FB799CDE",
            "codename": "gld1",
            "temperature": 68,
            "wet": False,
            "moved": True,
            "battery_percentage": 79,
        }
