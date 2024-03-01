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
            publish_state_response = await guardian.iot.publish_state()
            _LOGGER.info("publish_state command response: %s", publish_state_response)
        except GuardianError as err:
            _LOGGER.info(err)


asyncio.run(main())
