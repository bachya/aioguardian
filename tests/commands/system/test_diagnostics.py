"""Test the diagnostics command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("diagnostics_failure_response.json").encode()]
)
async def test_diagnostics_failure(mock_datagram_client):
    """Test the diagnostics command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.system.diagnostics()

    assert str(err.value) == (
        "system_diagnostics command failed "
        "(response: {'command': 1, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("diagnostics_success_response.json").encode()]
)
async def test_diagnostics_success(mock_datagram_client):
    """Test the diagnostics command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            diagnostics_response = await client.system.diagnostics()

        assert diagnostics_response["command"] == 1
        assert diagnostics_response["status"] == "ok"
        assert diagnostics_response["data"]["codename"] == "gvc1"
        assert diagnostics_response["data"]["uid"] == "ABCDEF123456"
        assert diagnostics_response["data"]["uptime"] == 41
        assert diagnostics_response["data"]["firmware"] == "0.20.9-beta+official.ef3"
        assert diagnostics_response["data"]["rf_modem_firmware"] == "4.0.0"
        assert diagnostics_response["data"]["available_heap"] == 34456
