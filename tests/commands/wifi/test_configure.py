"""Test the configure command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError, GuardianError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_configure_failure_response.json").encode()]
)
async def test_configure_failure(mock_datagram_client):
    """Test the wifi_configure command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.wifi.configure("My_Network", "password123")

        assert str(err.value) == (
            "wifi_configure command failed "
            "(response: {'command': 34, 'status': 'error'})"
        )


@pytest.mark.asyncio
async def test_configure_invalid_password(mock_datagram_client):
    """Test that an invalid password throws an exception."""
    with mock_datagram_client:
        with pytest.raises(GuardianError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.wifi.configure(
                    "My_Network",
                    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                )

        assert str(err.value) == (
            "Invalid parameters provided: length of value must be at most 64 for "
            "dictionary value @ data['password']"
        )


@pytest.mark.asyncio
async def test_configure_invalid_ssid(mock_datagram_client):
    """Test that an invalid SSID throws an exception."""
    with mock_datagram_client:
        with pytest.raises(GuardianError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.wifi.configure(
                    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "password123"
                )

        assert str(err.value) == (
            "Invalid parameters provided: length of value must be at most 36 for "
            "dictionary value @ data['ssid']"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("wifi_configure_success_response.json").encode()]
)
async def test_configure_success(mock_datagram_client):
    """Test the wifi_configure command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            wifi_configure_response = await client.wifi.configure(
                "My_Network", "password123"
            )

        assert wifi_configure_response["command"] == 34
        assert wifi_configure_response["status"] == "ok"
