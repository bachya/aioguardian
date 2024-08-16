"""Test the halt command."""

from unittest.mock import MagicMock, Mock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_halt_failure_response.json").encode()]
)
async def test_halt_failure(mock_datagram_client: MagicMock) -> None:
    """Test the valve_halt command failing.

    Args:
    ----
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.valve.halt()

        assert str(err.value) == "VALVE_HALT command failed: valve_already_stopped"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_halt_success_response.json").encode()]
)
async def test_halt_success(caplog: Mock, mock_datagram_client: MagicMock) -> None:
    """Test the valve_halt command succeeding.

    Args:
    ----
        caplog: A mocked logging facility.
        mock_datagram_client: A mocked UDP client.

    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            valve_halt_response = await client.valve.halt()

        assert valve_halt_response["command"] == 19
        assert any(
            "The device will not respond to leak events" in e.message
            for e in caplog.records
        )
