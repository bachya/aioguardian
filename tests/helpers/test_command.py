"""Test command helpers."""
import pytest

from aioguardian.errors import CommandError
from aioguardian.helpers.command import (
    Command,
    get_command_from_code,
    get_command_from_name,
)


@pytest.mark.asyncio
async def test_get_command_from_code() -> None:
    """Test the get_command_from_code helper."""
    real_command = get_command_from_code(0)
    assert real_command == Command.SYSTEM_PING

    with pytest.raises(CommandError) as err:
        _ = get_command_from_code(99999)
    assert str(err.value) == "Unknown command code: 99999"


@pytest.mark.asyncio
async def test_get_command_from_name() -> None:
    """Test the get_command_from_name helper."""
    real_command = get_command_from_name("SYSTEM_PING")
    assert real_command == Command.SYSTEM_PING

    with pytest.raises(CommandError) as err:
        _ = get_command_from_name("not real")
    assert str(err.value) == "Unknown command name: not real"
