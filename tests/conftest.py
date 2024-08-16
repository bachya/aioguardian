"""Define generic fixtures for tests."""

# pylint: disable=redefined-outer-name
from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture
def command_response() -> MagicMock:
    """Define a fixture for the JSON response payload of a command.

    Returns
    -------
        A mocked command response.

    """
    return MagicMock()


@pytest.fixture
def mock_datagram_client(recv_response: AsyncMock) -> Generator:
    """Define a mocked datagram client.

    Args:
    ----
        recv_response: A mocked instance of a socket recv operation.

    """
    mock_datagram_client = MagicMock()
    mock_datagram_client.connect = AsyncMock()
    mock_datagram_client.recv = recv_response
    mock_datagram_client.send = AsyncMock()
    mock_datagram_client.close = MagicMock()

    with patch("asyncio_dgram.connect", return_value=mock_datagram_client):
        yield mock_datagram_client


@pytest.fixture
def recv_response(command_response: MagicMock, remote_addr_response: str) -> AsyncMock:
    """Define a response from the socket.

    Returns
    -------
        A mocked instance of a socket recv operation.

    """
    return AsyncMock(return_value=(command_response, remote_addr_response))


@pytest.fixture
def remote_addr_response() -> str:
    """Define an IP address for the Guardian device.

    Returns
    -------
        A response for getting the valve's remote IP address.

    """
    return "192.168.1.100"
