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
            diagnostics_response = await guardian.system.diagnostics()
            _LOGGER.info("diagnostics command response: %s", diagnostics_response)

            onboard_sensor_status = await guardian.system.onboard_sensor_status()
            _LOGGER.info(
                "onboard_sensor_status command response: %s", onboard_sensor_status
            )

            ping_response = await guardian.system.ping()
            _LOGGER.info("ping command response: %s", ping_response)
        except GuardianError as err:
            _LOGGER.info(err)


asyncio.run(main())
