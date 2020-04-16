"""Test commands related to the device's valve."""
import pytest

from aioguardian import Client
from aioguardian.errors import CommandError

from tests.common import load_fixture


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_close_success_response.json").encode()]
)
async def test_valve_close_success(mock_datagram_client):
    """Test the valve_close command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            valve_close_response = await client.valve.valve_close()
        assert valve_close_response["command"] == 18


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_close_failure_response.json").encode()]
)
async def test_valve_close_failure(mock_datagram_client):
    """Test the valve_close command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.valve.valve_close()

    assert str(err.value) == "valve_close command failed: valve_already_closed"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_halt_success_response.json").encode()]
)
async def test_valve_halt_success(caplog, mock_datagram_client):
    """Test the valve_halt command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            valve_halt_response = await client.valve.valve_halt()
        assert valve_halt_response["command"] == 19
        assert any(
            "The device will not respond to leak events" in e.message
            for e in caplog.records
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_halt_failure_response.json").encode()]
)
async def test_valve_halt_failure(mock_datagram_client):
    """Test the valve_halt command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.valve.valve_halt()

    assert str(err.value) == "valve_halt command failed: valve_already_stopped"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_status_success_response.json").encode()]
)
async def test_valve_status_success(mock_datagram_client):
    """Test the valve_status command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            valve_status_response = await client.valve.valve_status()
        assert valve_status_response["command"] == 16
        assert valve_status_response["status"] == "ok"
        valve_status_response["data"]["enabled"] = False
        valve_status_response["data"]["direction"] = True
        valve_status_response["data"]["state"] = "default"
        valve_status_response["data"]["travel_count"] = 0
        valve_status_response["data"]["instantaneous_current"] = 0
        valve_status_response["data"]["instantaneous_current_ddt"] = 0
        valve_status_response["data"]["average_current"] = 34


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_status_failure_response.json").encode()]
)
async def test_valve_status_failure(mock_datagram_client):
    """Test the valve_status command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.valve.valve_status()

    assert str(err.value) == (
        "valve_status command failed (response: {'command': 16, 'status': 'error'})"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_open_success_response.json").encode()]
)
async def test_valve_open_success(mock_datagram_client):
    """Test the valve_open command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            valve_open_response = await client.valve.valve_open()
        assert valve_open_response["command"] == 17


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_open_failure_response.json").encode()]
)
async def test_valve_open_failure(mock_datagram_client):
    """Test the valve_open command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.valve.valve_open()

    assert str(err.value) == "valve_open command failed: valve_moving"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_status_success_response.json").encode()]
)
async def test_valve_status_success(mock_datagram_client):
    """Test the valve_status command succeeding."""
    with mock_datagram_client:
        async with Client("192.168.1.100") as client:
            valve_status_response = await client.valve.valve_status()
        assert valve_status_response["command"] == 16
        assert valve_status_response["status"] == "ok"
        valve_status_response["data"]["enabled"] = False
        valve_status_response["data"]["direction"] = True
        valve_status_response["data"]["state"] = "default"
        valve_status_response["data"]["travel_count"] = 0
        valve_status_response["data"]["instantaneous_current"] = 0
        valve_status_response["data"]["instantaneous_current_ddt"] = 0
        valve_status_response["data"]["average_current"] = 34


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("valve_status_failure_response.json").encode()]
)
async def test_valve_status_failure(mock_datagram_client):
    """Test the valve_status command failing."""
    with mock_datagram_client:
        with pytest.raises(CommandError) as err:
            async with Client("192.168.1.100") as client:
                _ = await client.valve.valve_status()

    assert str(err.value) == (
        "valve_status command failed (response: {'command': 16, 'status': 'error'})"
    )
