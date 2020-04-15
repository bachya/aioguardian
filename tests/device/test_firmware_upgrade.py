"""Test the upgrade_firmware command."""
from asynctest import CoroutineMock, MagicMock, patch
import pytest

from aioguardian import Client
from aioguardian.errors import RequestError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("upgrade_firmware_success_response.json").encode()],
)
async def test_upgrade_firmware_success_async(mock_datagram_client):
    """Test successfully getting upgrade_firmware info in async mode."""
    client = Client("192.168.1.100", use_async=True)
    with mock_datagram_client:
        upgrade_firmware_response = await client.device.upgrade_firmware()
        assert upgrade_firmware_response["command"] == 4
        assert upgrade_firmware_response["status"] == "ok"


@pytest.mark.parametrize(
    "command_response",
    [load_fixture("upgrade_firmware_success_response.json").encode()],
)
def test_upgrade_firmware_success_sync(mock_datagram_client):
    """Test successfully getting upgrade_firmware info in sync mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        upgrade_firmware_response = client.device.upgrade_firmware()
        assert upgrade_firmware_response["command"] == 4
        assert upgrade_firmware_response["status"] == "ok"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("upgrade_firmware_failure_response.json").encode()],
)
async def test_upgrade_firmware_failure_async(mock_datagram_client):
    """Test the upgrade_firmware command failing in async mode."""
    client = Client("192.168.1.100", use_async=True)
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            await client.device.upgrade_firmware()
            assert "error" in err


@pytest.mark.parametrize(
    "command_response",
    [load_fixture("upgrade_firmware_failure_response.json").encode()],
)
def test_upgrade_firmware_failure_sync(mock_datagram_client):
    """Test the upgrade_firmware command failing in sync mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            client.device.upgrade_firmware()
            assert "error" in err
