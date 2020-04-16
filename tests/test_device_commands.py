"""Test commands related to the device itself."""
from asynctest import CoroutineMock, patch
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError, GuardianError

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
                _ = await client.device.diagnostics()

    assert str(err.value) == (
        "diagnostics command failed (response: {'command': 1, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("diagnostics_success_response.json").encode()]
)
async def test_diagnostics_success(mock_datagram_client):
    """Test the diagnostics command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            diagnostics_response = await client.device.diagnostics()
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
    "command_response", [load_fixture("factory_reset_failure_response.json").encode()]
)
async def test_factory_reset_failure(mock_datagram_client):
    """Test the factory_reset command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.device.factory_reset()

    assert str(err.value) == (
        "factory_reset command failed (response: {'command': 255, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("factory_reset_success_response.json").encode()]
)
async def test_factory_reset_success(mock_datagram_client):
    """Test the factory_reset command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            factory_reset_response = await client.device.factory_reset()
        assert factory_reset_response["command"] == 255
        assert factory_reset_response["status"] == "ok"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("upgrade_firmware_failure_response.json").encode()],
)
async def test_upgrade_firmware_failure(mock_datagram_client):
    """Test the upgrade_firmware command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.device.upgrade_firmware()
            client.disconnect()

    assert str(err.value) == (
        "upgrade_firmware command failed (response: {'command': 4, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("upgrade_firmware_success_response.json").encode()],
)
async def test_upgrade_firmware_success(mock_datagram_client):
    """Test the upgrade_firmware command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            upgrade_firmware_response = await client.device.upgrade_firmware()
        assert upgrade_firmware_response["command"] == 4
        assert upgrade_firmware_response["status"] == "ok"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_failure_response.json").encode()]
)
async def test_ping_failure(mock_datagram_client):
    """Test a failured ping of the device."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.device.ping()

    assert str(err.value) == (
        "ping command failed (response: {'command': 0, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_success_response.json").encode()]
)
async def test_ping_success(mock_datagram_client):
    """Test the ping command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            ping_response = await client.device.ping()
        assert ping_response["command"] == 0
        assert ping_response["status"] == "ok"
        assert ping_response["data"]["uid"] == "ABCDEF123456"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("reboot_failure_response.json").encode()]
)
async def test_reboot_failure(mock_datagram_client):
    """Test the reboot command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.device.reboot()

    assert str(err.value) == (
        "reboot command failed (response: {'command': 2, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("reboot_success_response.json").encode()]
)
async def test_reboot_success(mock_datagram_client):
    """Test the reboot command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            # Patch asyncio.sleep so that this test doesn't take 3-ish seconds:
            with patch("asyncio.sleep", CoroutineMock()):
                reboot_response = await client.device.reboot()
        assert reboot_response["command"] == 2
        assert reboot_response["status"] == "ok"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_configure_failure_response.json").encode()]
)
async def test_wifi_configure_failure(mock_datagram_client):
    """Test the wifi_configure command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.device.wifi_configure("My_Network", "password123")

    assert str(err.value) == (
        "wifi_configure command failed (response: {'command': 34, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_configure_success_response.json").encode()]
)
async def test_wifi_configure_success(mock_datagram_client):
    """Test the wifi_configure command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            wifi_configure_response = await client.device.wifi_configure(
                "My_Network", "password123"
            )
        assert wifi_configure_response["command"] == 34
        assert wifi_configure_response["status"] == "ok"


@pytest.mark.asyncio
async def test_wifi_configure_invalid_password(mock_datagram_client):
    """Test the wifi_configure command failing."""
    with mock_datagram_client:
        with pytest.raises(GuardianError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.device.wifi_configure(
                    "My_Network",
                    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                )

    assert str(err.value) == (
        "Invalid parameters provided: WiFi password has a max length of 64 "
        "for dictionary value @ data['password']"
    )


@pytest.mark.asyncio
async def test_wifi_configure_invalid_ssid(mock_datagram_client):
    """Test the wifi_configure command failing."""
    with mock_datagram_client:
        with pytest.raises(GuardianError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.device.wifi_configure(
                    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "password123"
                )

    assert str(err.value) == (
        "Invalid parameters provided: WiFi SSID has a max length of 36 "
        "for dictionary value @ data['ssid']"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_reset_failure_response.json").encode()]
)
async def test_wifi_reset_failure(mock_datagram_client):
    """Test the wifi_reset command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.device.wifi_reset()

    assert str(err.value) == (
        "wifi_reset command failed (response: {'command': 33, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_reset_success_response.json").encode()]
)
async def test_wifi_reset_success(mock_datagram_client):
    """Test the wifi_reset command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            wifi_reset_response = await client.device.wifi_reset()
        assert wifi_reset_response["command"] == 33
        assert wifi_reset_response["status"] == "ok"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_status_failure_response.json").encode()]
)
async def test_wifi_status_failure(mock_datagram_client):
    """Test the wifi_status command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.device.wifi_status()

    assert str(err.value) == (
        "wifi_status command failed (response: {'command': 32, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_status_success_response.json").encode()]
)
async def test_wifi_status_success(mock_datagram_client):
    """Test the wifi_status command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            wifi_status_response = await client.device.wifi_status()
        assert wifi_status_response["command"] == 32
        assert wifi_status_response["status"] == "ok"
        assert wifi_status_response["data"]["station_connected"] is True
        assert wifi_status_response["data"]["ip_assigned"] is True
        assert wifi_status_response["data"]["mqtt_connected"] is True
        assert wifi_status_response["data"]["rssi"] == -63
        assert wifi_status_response["data"]["channel"] == 1
        assert wifi_status_response["data"]["lan_ipv4"] == "192.168.1.100"
        assert (
            wifi_status_response["data"]["lan_ipv6"]
            == "AC10:BD0:FFFF:FFFF:AC10:BD0:FFFF:FFFF"
        )
        assert wifi_status_response["data"]["ap_enabled"] is True
        assert wifi_status_response["data"]["ap_clients"] == 0
        assert wifi_status_response["data"]["bssid"] == "ABCDEF123456"
        assert wifi_status_response["data"]["ssid"] == "My_Network"
