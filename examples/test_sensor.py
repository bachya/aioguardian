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
            pair_dump_response = await guardian.sensor.pair_dump()
            _LOGGER.info("pair_dump_response command response: %s", pair_dump_response)

            for uid in pair_dump_response["data"]["paired_uids"]:
                paired_sensor_status_resp = await guardian.sensor.paired_sensor_status(
                    uid
                )
                _LOGGER.info(
                    "paired_sensor_status command response (UID: %s): %s",
                    uid,
                    paired_sensor_status_resp,
                )
        except GuardianError as err:
            _LOGGER.info(err)


asyncio.run(main())
