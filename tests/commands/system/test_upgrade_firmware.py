"""Test the upgrade_firmware command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError, GuardianError

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
                _ = await client.system.upgrade_firmware()
            client.disconnect()

        assert str(err.value) == (
            "system_upgrade_firmware command failed "
            "(response: {'command': 4, 'status': 'error'})"
        )


@pytest.mark.asyncio
async def test_upgrade_firmware_invalid_filename(mock_datagram_client):
    """Test that an invalid firmware filename throws an exception."""
    with mock_datagram_client:
        with pytest.raises(GuardianError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.system.upgrade_firmware(
                    filename="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                )

        assert str(err.value) == (
            "Invalid parameters provided: length of value must be at most 48 for "
            "dictionary value @ data['filename']"
        )


@pytest.mark.asyncio
async def test_upgrade_firmware_invalid_port(mock_datagram_client):
    """Test that an invalid firmware port throws an exception."""
    with mock_datagram_client:
        with pytest.raises(GuardianError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.system.upgrade_firmware(port="WHOOPS")

        assert str(err.value) == (
            "Invalid parameters provided: expected int for dictionary value @ "
            "data['port']"
        )


@pytest.mark.asyncio
async def test_upgrade_firmware_invalid_url(mock_datagram_client):
    """Test that an invalid firmware URL throws an exception."""
    with mock_datagram_client:
        with pytest.raises(GuardianError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.system.upgrade_firmware(url="not_real_url")

        assert str(err.value) == (
            "Invalid parameters provided: Invalid URL for dictionary value @ "
            "data['url']"
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
            upgrade_firmware_response = await client.system.upgrade_firmware()

        assert upgrade_firmware_response["command"] == 4
        assert upgrade_firmware_response["status"] == "ok"
