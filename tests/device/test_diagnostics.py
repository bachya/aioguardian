"""Test the diagnostics command."""
from asynctest import CoroutineMock, MagicMock, patch
import pytest

from aioguardian import Client
from aioguardian.errors import RequestError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("diagnostics_success_response.json").encode()]
)
async def test_diagnostics_success_async(mock_datagram_client):
    """Test successfully getting diagnostics info in async mode."""
    client = Client("192.168.1.100", use_async=True)
    with mock_datagram_client:
        diagnostics_response = await client.device.diagnostics()
        assert diagnostics_response["command"] == 1
        assert diagnostics_response["status"] == "ok"
        assert diagnostics_response["data"]["codename"] == "gvc1"
        assert diagnostics_response["data"]["uid"] == "ABCDEF123456"
        assert diagnostics_response["data"]["uptime"] == 41
        assert diagnostics_response["data"]["firmware"] == "0.20.9-beta+official.ef3"
        assert diagnostics_response["data"]["rf_modem_firmware"] == "4.0.0"
        assert diagnostics_response["data"]["available_heap"] == 34456


@pytest.mark.parametrize(
    "command_response", [load_fixture("diagnostics_success_response.json").encode()]
)
def test_diagnostics_success_sync(mock_datagram_client):
    """Test successfully getting diagnostics info in sync mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        diagnostics_response = client.device.diagnostics()
        assert diagnostics_response["command"] == 1
        assert diagnostics_response["status"] == "ok"
        assert diagnostics_response["data"]["codename"] == "gvc1"
        assert diagnostics_response["data"]["uid"] == "ABCDEF123456"
        assert diagnostics_response["data"]["uptime"] == 41
        assert diagnostics_response["data"]["firmware"] == "0.20.9-beta+official.ef3"
        assert diagnostics_response["data"]["rf_modem_firmware"] == "4.0.0"
        assert diagnostics_response["data"]["available_heap"] == 34456


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("diagnostics_failure_response.json").encode()]
)
async def test_diagnostics_failure_async(mock_datagram_client):
    """Test the diagnostics command failing in async mode."""
    client = Client("192.168.1.100", use_async=True)
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            await client.device.diagnostics()
            assert "error" in err


@pytest.mark.parametrize(
    "command_response", [load_fixture("diagnostics_failure_response.json").encode()]
)
def test_diagnostics_failure_sync(mock_datagram_client):
    """Test the diagnostics command failing in sync mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            client.device.diagnostics()
            assert "error" in err
