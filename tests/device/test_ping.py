"""Test the ping command."""
from asynctest import CoroutineMock, MagicMock, patch
import pytest

from aioguardian import Client
from aioguardian.errors import RequestError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_success_response.json").encode()]
)
async def test_ping_success_async(mock_datagram_client):
    """Test a successful ping of the device in async mode."""
    client = Client("192.168.1.100", use_async=True)
    with mock_datagram_client:
        ping_response = await client.device.ping()
        assert ping_response["command"] == 0
        assert ping_response["status"] == "ok"
        assert ping_response["data"]["uid"] == "ABCDEF123456"


@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_success_response.json").encode()]
)
def test_ping_success_sync(mock_datagram_client):
    """Test a successful ping of the device in sync mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        ping_response = client.device.ping()
        assert ping_response["command"] == 0
        assert ping_response["status"] == "ok"
        assert ping_response["data"]["uid"] == "ABCDEF123456"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_failure_response.json").encode()]
)
async def test_ping_failure_async(mock_datagram_client):
    """Test a failureful ping of the device in async mode."""
    client = Client("192.168.1.100", use_async=True)
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            await client.device.ping()
            assert "error" in err


@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_failure_response.json").encode()]
)
def test_ping_failure_sync(mock_datagram_client):
    """Test a failureful ping of the device in sync mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            client.device.ping()
            assert "error" in err
