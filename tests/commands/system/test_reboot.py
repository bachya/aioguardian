"""Test the reboot command."""
from asynctest import CoroutineMock, patch
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("reboot_failure_response.json").encode()]
)
async def test_reboot_failure(mock_datagram_client):
    """Test the reboot command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.system.reboot()

        assert str(err.value) == (
            "system_reboot command failed (response: {'command': 2, 'status': 'error'})"
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
                reboot_response = await client.system.reboot()

        assert reboot_response["command"] == 2
        assert reboot_response["status"] == "ok"
