"""Test the reset command."""

from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_reset_failure_response.json").encode()]
)
async def test_reset_failure(mock_datagram_client: MagicMock) -> None:
    """Test the valve_reset command failing.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.valve.reset()

        assert (
            str(err.value) == "VALVE_RESET command failed "
            "(response: {'command': 20, 'status': 'error'})"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_reset_success_response.json").encode()]
)
async def test_reset_success(mock_datagram_client: MagicMock) -> None:
    """Test the valve_reset command succeeding.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            valve_reset_response = await client.valve.reset()

        assert valve_reset_response["command"] == 20
