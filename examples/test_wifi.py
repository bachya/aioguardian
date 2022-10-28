"""Run an example script to quickly test the guardian."""
import asyncio
import logging

from aioguardian import Client
from aioguardian.errors import GuardianError

_LOGGER = logging.getLogger(__name__)


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)

    async with Client("172.16.11.208") as guardian:
        try:
            wifi_status_response = await guardian.wifi.status()
            _LOGGER.info("wifi_status command response: %s", wifi_status_response)
        except GuardianError as err:
            _LOGGER.info(err)


asyncio.run(main())
