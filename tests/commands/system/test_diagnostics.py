"""Test the diagnostics command."""

from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("diagnostics_failure_response.json").encode()]
)
async def test_diagnostics_failure(mock_datagram_client: MagicMock) -> None:
    """Test the diagnostics command failing.

    Args:
        mock_datagram_client: A mocked UDP client.
    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.system.diagnostics()

        assert str(err.value) == (
            "SYSTEM_DIAGNOSTICS command failed "
            "(response: {'command': 1, 'status': 'error'})"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("diagnostics_success_response.json").encode()]
)
async def test_diagnostics_success(mock_datagram_client: MagicMock) -> None:
    """Test the diagnostics command succeeding.

    Args:
        mock_datagram_client: A mocked UDP client.
    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            diagnostics_response = await client.system.diagnostics()

        assert diagnostics_response["command"] == 1
        assert diagnostics_response["status"] == "ok"
        assert diagnostics_response["data"] == {
            "codename": "gvc1",
            "uid": "ABCDEF123456",
            "uptime": 41,
            "firmware": "0.20.9-beta+official.ef3",
            "rf_modem_firmware": "4.0.0",
            "available_heap": 34456,
        }
