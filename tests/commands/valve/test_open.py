"""Test the open command."""

from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_open_failure_response.json").encode()]
)
async def test_open_failure(mock_datagram_client: MagicMock) -> None:
    """Test the valve_open command failing.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.valve.open()

        assert str(err.value) == "VALVE_OPEN command failed: valve_moving"


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_open_success_response.json").encode()]
)
async def test_open_success(mock_datagram_client: MagicMock) -> None:
    """Test the valve_open command succeeding.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            valve_open_response = await client.valve.open()

        assert valve_open_response["command"] == 17
