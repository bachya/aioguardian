"""Test the pair_dump command."""
from unittest.mock import MagicMock

import pytest

from aioguardian import Client
from aioguardian.errors import CommandError
from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("pair_dump_failure_response.json").encode()]
)
async def test_pair_dump_failure(mock_datagram_client: MagicMock) -> None:
    """Test the pair_dump command failing.

    Args:
        mock_datagram_client: A mocked UDP client.
    """
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.sensor.pair_dump()

        assert str(err.value) == (
            "SENSOR_PAIR_DUMP command failed "
            "(response: {'command': 48, 'status': 'error'})"
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("pair_dump_success_response.json").encode()]
)
async def test_pair_dump_success(mock_datagram_client: MagicMock) -> None:
    """Test the pair_dump command succeeding.

    Args:
        mock_datagram_client: A mocked UDP client.
    """
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            pair_dump_response = await client.sensor.pair_dump()

        assert pair_dump_response["command"] == 48
        assert pair_dump_response["status"] == "ok"
        assert pair_dump_response["data"] == {
            "pair_count": 1,
            "paired_uids": ["6309FB799CDE"],
        }
