"""Run an example script to quickly test."""
import logging
import time

from aioguardian import Client
from aioguardian.errors import GuardianError

_LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.DEBUG)

    client = Client("172.16.11.208")

    start = time.time()

    try:
        # Run through various device-related commands:
        ping_response = client.device.ping()
        _LOGGER.info("Ping response: %s", ping_response)

        diagnostics_response = client.device.diagnostics()
        _LOGGER.info("Diagnostics response: %s", diagnostics_response)
    except GuardianError as err:
        _LOGGER.info(err)

    end = time.time()

    _LOGGER.info("Execution time: %s seconds", end - start)


main()
