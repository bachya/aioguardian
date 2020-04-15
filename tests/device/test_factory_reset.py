"""Test the factory_reset command."""
from asynctest import CoroutineMock, MagicMock, patch
import pytest

from aioguardian import Client
from aioguardian.errors import RequestError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("factory_reset_success_response.json").encode()]
)
async def test_factory_reset_success_async(mock_datagram_client):
    """Test successfully getting factory_reset info in async mode."""
    client = Client("192.168.1.100", use_async=True)
    with mock_datagram_client:
        factory_reset_response = await client.device.factory_reset()
        assert factory_reset_response["command"] == 255
        assert factory_reset_response["status"] == "ok"


@pytest.mark.parametrize(
    "command_response", [load_fixture("factory_reset_success_response.json").encode()]
)
def test_factory_reset_success_sync(mock_datagram_client):
    """Test successfully getting factory_reset info in sync mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        factory_reset_response = client.device.factory_reset()
        assert factory_reset_response["command"] == 255
        assert factory_reset_response["status"] == "ok"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("factory_reset_failure_response.json").encode()]
)
async def test_factory_reset_failure_async(mock_datagram_client):
    """Test the factory_reset command failing in async mode."""
    client = Client("192.168.1.100", use_async=True)
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            await client.device.factory_reset()
            assert "error" in err


@pytest.mark.parametrize(
    "command_response", [load_fixture("factory_reset_failure_response.json").encode()]
)
def test_factory_reset_failure_sync(mock_datagram_client):
    """Test the factory_reset command failing in sync mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            client.device.factory_reset()
            assert "error" in err
