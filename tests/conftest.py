"""Define generic fixtures for tests."""
# pylint: disable=redefined-outer-name
import pytest

from tests.async_mock import AsyncMock, MagicMock, patch


@pytest.fixture()
def command_response():
    """Define a fixture for the JSON response payload of a command."""
    return MagicMock()


@pytest.fixture()
def mock_datagram_client(recv_response):
    """Define a mocked datagram client."""
    mock_datagram_client = MagicMock()
    mock_datagram_client.connect = AsyncMock()
    mock_datagram_client.recv = recv_response
    mock_datagram_client.send = AsyncMock()
    mock_datagram_client.close = MagicMock()

    with patch("asyncio_dgram.connect", return_value=mock_datagram_client):
        yield mock_datagram_client


@pytest.fixture()
def recv_response(command_response, remote_addr_response):
    """Define a response from the socket."""
    return AsyncMock(return_value=(command_response, remote_addr_response))


@pytest.fixture()
def remote_addr_response():
    """Define an IP address for the Guardian device."""
    return "192.168.1.100"
