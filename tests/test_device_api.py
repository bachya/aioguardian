"""Test device-related API calls."""
import asyncio

from asynctest import CoroutineMock, MagicMock, patch
import pytest

from aioguardian import Client
from aioguardian.client import _get_event_loop
from aioguardian.errors import RequestError

from .common import load_fixture


def test_get_event_loop():
    """Test getting the active (or a new) event loop."""
    loop = _get_event_loop()  # pylint: disable=protected-access
    assert isinstance(loop, asyncio.AbstractEventLoop)

    # Test there being no currently running event loop generates one:
    with patch("asyncio.get_event_loop", side_effect=RuntimeError):
        loop = _get_event_loop()  # pylint: disable=protected-access
        assert isinstance(loop, asyncio.AbstractEventLoop)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_success_response.json").encode()]
)
async def test_ping_success_async(mock_datagram_client):
    """Test a successful ping of the device in async mode."""
    client = Client("192.168.1.100", use_async=True)
    with mock_datagram_client:
        ping_response = await client.device.ping()
        assert ping_response["command"] == 0
        assert ping_response["status"] == "ok"
        assert ping_response["data"]["uid"] == "ABCDEF123456"


@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_success_response.json").encode()]
)
def test_ping_success_sync(mock_datagram_client):
    """Test a successful ping of the device in sync mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        ping_response = client.device.ping()
        assert ping_response["command"] == 0
        assert ping_response["status"] == "ok"
        assert ping_response["data"]["uid"] == "ABCDEF123456"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_failure_response.json").encode()]
)
async def test_ping_failure_async(mock_datagram_client):
    """Test a failureful ping of the device in async mode."""
    client = Client("192.168.1.100", use_async=True)
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            await client.device.ping()
            assert "error" in err


@pytest.mark.parametrize(
    "command_response", [load_fixture("ping_failure_response.json").encode()]
)
def test_ping_failure_sync(mock_datagram_client):
    """Test a failureful ping of the device in sync mode."""
    client = Client("192.168.1.100")
    with mock_datagram_client:
        with pytest.raises(RequestError) as err:
            client.device.ping()
            assert "error" in err
