"""Test the ununpair_sensor command."""

from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "command_response", [load_fixture("unpair_sensor_failure_response.json").encode()]
)
async def test_unpair_sensor_failure(mock_datagram_client: MagicMock) -> None:
    """Test the unpair_sensor command failing.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.sensor.unpair_sensor("abc123")

        assert str(err.value) == (
            "SENSOR_UNPAIR_SENSOR command failed "
            "(response: {'command': 50, 'status': 'error'})"
        )


@pytest.mark.asyncio()
async def test_unpair_sensor_invalid_uid(mock_datagram_client: MagicMock) -> None:
    """Test that an invalid UID throws an exception.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.sensor.unpair_sensor("$@&*!@--")

        assert str(err.value) == (
            "Invalid parameters provided: String is not alphanumeric for dictionary "
            "value @ data['uid']"
        )


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "command_response", [load_fixture("unpair_sensor_success_response.json").encode()]
)
async def test_unpair_sensor_success(mock_datagram_client: MagicMock) -> None:
    """Test the unpair_sensor command succeeding.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            unpair_sensor_response = await client.sensor.unpair_sensor("abc123")

        assert unpair_sensor_response["command"] == 50
        assert unpair_sensor_response["status"] == "ok"
