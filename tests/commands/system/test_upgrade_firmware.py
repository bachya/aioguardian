"""Test the upgrade_firmware command."""
from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import GuardianError
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("upgrade_firmware_success_response.json").encode()],
)
async def test_upgrade_firmware_custom_parameters(
    mock_datagram_client: MagicMock,
) -> None:
    """Test that valid custom parameters work.

    Args:
        mock_datagram_client: A mocked UDP client.
    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            upgrade_firmware_response = await client.system.upgrade_firmware(
                url="https://firmware.com", port=8080, filename="123.bin"
            )

        assert upgrade_firmware_response["command"] == 4
        assert upgrade_firmware_response["status"] == "ok"


@pytest.mark.asyncio
async def test_upgrade_firmware_invalid_filename(
    mock_datagram_client: MagicMock,
) -> None:
    """Test that an invalid firmware filename throws an exception.

    Args:
        mock_datagram_client: A mocked UDP client.
    """
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
async def test_upgrade_firmware_invalid_port(mock_datagram_client: MagicMock) -> None:
    """Test that an invalid firmware port throws an exception.

    Args:
        mock_datagram_client: A mocked UDP client.
    """
    with mock_datagram_client:
        with pytest.raises(GuardianError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.system.upgrade_firmware(
                    port="WHOOPS"  # type: ignore[arg-type]
                )

        assert str(err.value) == (
            "Invalid parameters provided: expected int for dictionary value @ "
            "data['port']"
        )


@pytest.mark.asyncio
async def test_upgrade_firmware_invalid_url(mock_datagram_client: MagicMock) -> None:
    """Test that an invalid firmware URL throws an exception.

    Args:
        mock_datagram_client: A mocked UDP client.
    """
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
async def test_upgrade_firmware_success(mock_datagram_client: MagicMock) -> None:
    """Test the upgrade_firmware command succeeding.

    Args:
        mock_datagram_client: A mocked UDP client.
    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            upgrade_firmware_response = await client.system.upgrade_firmware()

        assert upgrade_firmware_response["command"] == 4
        assert upgrade_firmware_response["status"] == "ok"
