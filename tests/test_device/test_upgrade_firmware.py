"""Test the upgrade_firmware command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


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
