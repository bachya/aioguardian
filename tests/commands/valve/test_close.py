"""Test the close command."""

from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_close_failure_response.json").encode()]
)
async def test_close_failure(mock_datagram_client: MagicMock) -> None:
    """Test the valve_close command failing.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.valve.close()

        assert str(err.value) == "VALVE_CLOSE command failed: valve_already_closed"


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_close_success_response.json").encode()]
)
async def test_close_success(mock_datagram_client: MagicMock) -> None:
    """Test the valve_close command succeeding.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            valve_close_response = await client.valve.close()

        assert valve_close_response["command"] == 18
