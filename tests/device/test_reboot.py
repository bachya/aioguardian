"""Test the reboot command."""
from asynctest import CoroutineMock, MagicMock, patch
import pytest

from aioguardian import Client
from aioguardian.errors import RequestError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("reboot_success_response.json").encode()]
)
async def test_reboot_success_async(mock_datagram_client):
    """Test successfully getting reboot info in async mode."""
    client = Client("192.168.1.100", use_async=True)
    with mock_datagram_client:
        reboot_response = await client.device.reboot()
        assert reboot_response["command"] == 2
        assert reboot_response["status"] == "ok"


@pytest.mark.parametrize(
    "command_response", [load_fixture("reboot_success_response.json").encode()]
)
def test_reboot_success_sync(mock_datagram_client):
    """Test successfully getting reboot info in sync mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        reboot_response = client.device.reboot()
        assert reboot_response["command"] == 2
        assert reboot_response["status"] == "ok"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("reboot_failure_response.json").encode()]
)
async def test_reboot_failure_async(mock_datagram_client):
    """Test the reboot command failing in async mode."""
    client = Client("192.168.1.100", use_async=True)
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            await client.device.reboot()
            assert "error" in err


@pytest.mark.parametrize(
    "command_response", [load_fixture("reboot_failure_response.json").encode()]
)
def test_reboot_failure_sync(mock_datagram_client):
    """Test the reboot command failing in sync mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            client.device.reboot()
            assert "error" in err
