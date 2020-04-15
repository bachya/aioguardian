"""Run an example script to quickly test."""
import logging
import time

from aioguardian import Client
from aioguardian.errors import GuardianError

_LOGGER = logging.getLogger(__name__)


def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.DEBUG)

    client = Client("<IP ADDRESS>")

    start = time.time()

    try:
        # Get current UV info:
        ping_response = client.device.ping()
        _LOGGER.info("Ping response: %s", ping_response)
    except GuardianError as err:
        _LOGGER.info(err)

    end = time.time()

    _LOGGER.info("Execution time: %s seconds", end - start)


main()
