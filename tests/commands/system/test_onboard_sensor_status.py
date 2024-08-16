"""Test the onboard_sensor_status command."""

from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("onboard_sensor_status_success_response.json").encode()],
)
async def test_onboard_sensor_status_success(mock_datagram_client: MagicMock) -> None:
    """Test the onboard_sensor_status command succeeding.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            onboard_sensor_status = await client.system.onboard_sensor_status()

        assert onboard_sensor_status["command"] == 80
        assert onboard_sensor_status["status"] == "ok"
        assert onboard_sensor_status["data"] == {"temperature": 71, "wet": False}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("onboard_sensor_status_failure_response.json").encode()],
)
async def test_onboard_sensor_status_failure(mock_datagram_client: MagicMock) -> None:
    """Test the onboard_sensor_status command failing.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.system.onboard_sensor_status()

        assert str(err.value) == (
            "SYSTEM_ONBOARD_SENSOR_STATUS command failed "
            "(response: {'command': 80, 'status': 'error'})"
        )
