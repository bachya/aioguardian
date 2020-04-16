"""Test commands related to the device itself."""
from asynctest import CoroutineMock, MagicMock, patch
import pytest

from aioguardian import Client
from aioguardian.errors import RequestError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("diagnostics_success_response.json").encode()]
)
async def test_diagnostics_success(mock_datagram_client):
    """Test successfully getting diagnostics info in async mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        await client.connect()
        diagnostics_response = await client.device.diagnostics()
        client.disconnect()
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
async def test_diagnostics_failure(mock_datagram_client):
    """Test the diagnostics command failing in async mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            await client.connect()
            _ = await client.device.diagnostics()
            client.disconnect()
            assert "error" in err


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("factory_reset_success_response.json").encode()]
)
async def test_factory_reset_success(mock_datagram_client):
    """Test successfully getting factory_reset info in async mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        await client.connect()
        factory_reset_response = await client.device.factory_reset()
        client.disconnect()
        assert factory_reset_response["command"] == 255
        assert factory_reset_response["status"] == "ok"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("factory_reset_failure_response.json").encode()]
)
async def test_factory_reset_failure(mock_datagram_client):
    """Test the factory_reset command failing in async mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            await client.connect()
            _ = await client.device.factory_reset()
            client.disconnect()
            assert "error" in err


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("upgrade_firmware_success_response.json").encode()],
)
async def test_upgrade_firmware_success(mock_datagram_client):
    """Test successfully getting upgrade_firmware info in async mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        await client.connect()
        upgrade_firmware_response = await client.device.upgrade_firmware()
        client.disconnect()
        assert upgrade_firmware_response["command"] == 4
        assert upgrade_firmware_response["status"] == "ok"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("upgrade_firmware_failure_response.json").encode()],
)
async def test_upgrade_firmware_failure(mock_datagram_client):
    """Test the upgrade_firmware command failing in async mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            await client.connect()
            _ = await client.device.upgrade_firmware()
            client.disconnect()
            assert "error" in err


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_success_response.json").encode()]
)
async def test_ping_success(mock_datagram_client):
    """Test a successful ping of the device in async mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        await client.connect()
        ping_response = await client.device.ping()
        client.disconnect()
        assert ping_response["command"] == 0
        assert ping_response["status"] == "ok"
        assert ping_response["data"]["uid"] == "ABCDEF123456"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_failure_response.json").encode()]
)
async def test_ping_failure(mock_datagram_client):
    """Test a failureful ping of the device in async mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            await client.connect()
            _ = await client.device.ping()
            client.disconnect()
            assert "error" in err


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("reboot_success_response.json").encode()]
)
async def test_reboot_success(mock_datagram_client):
    """Test successfully getting reboot info in async mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        await client.connect()
        reboot_response = await client.device.reboot()
        client.disconnect()
        assert reboot_response["command"] == 2
        assert reboot_response["status"] == "ok"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("reboot_failure_response.json").encode()]
)
async def test_reboot_failure(mock_datagram_client):
    """Test the reboot command failing in async mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            await client.connect()
            _ = await client.device.reboot()
            client.disconnect()
            assert "error" in err
