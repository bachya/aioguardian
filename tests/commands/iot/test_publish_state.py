"""Test the publish_state command."""
from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("publish_state_failure_response.json").encode()],
)
async def test_publish_state_failure(mock_datagram_client: MagicMock) -> None:
    """Test the publish_state command failing.

    Args:
        mock_datagram_client: A mocked UDP client.
    """
    with mock_datagram_client, pytest.raises(CommandError) as err:
        async with Client("192.168.1.100") as client:
            _ = await client.iot.publish_state()
        client.disconnect()

    assert str(err.value) == (
        "IOT_PUBLISH_STATE command failed "
        "(response: {'command': 65, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response",
    [load_fixture("publish_state_success_response.json").encode()],
)
async def test_publish_state_success(mock_datagram_client: MagicMock) -> None:
    """Test the publish_state command succeeding.

    Args:
        mock_datagram_client: A mocked UDP client.
    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            publish_state_response = await client.iot.publish_state()

        assert publish_state_response["command"] == 65
        assert publish_state_response["status"] == "ok"
