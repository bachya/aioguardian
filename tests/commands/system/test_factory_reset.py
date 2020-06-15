"""Test the factory_reset command."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("factory_reset_failure_response.json").encode()]
)
async def test_factory_reset_failure(mock_datagram_client):
    """Test the factory_reset command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.system.factory_reset()

    assert str(err.value) == (
        "system_factory_reset command failed "
        "(response: {'command': 255, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("factory_reset_success_response.json").encode()]
)
async def test_factory_reset_success(mock_datagram_client):
    """Test the factory_reset command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            factory_reset_response = await client.system.factory_reset()

        assert factory_reset_response["command"] == 255
        assert factory_reset_response["status"] == "ok"
