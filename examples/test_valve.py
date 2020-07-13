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
            valve_status_response = await guardian.valve.status()
            _LOGGER.info(
                "valve_status_response command response: %s", valve_status_response
            )

            valve_open_response = await guardian.valve.open()
            _LOGGER.info(
                "valve_open_response command response: %s", valve_open_response
            )

            # Give the valve a chance to open fully so that the valve_close command
            # doesn't error out:
            await asyncio.sleep(3)

            valve_close_response = await guardian.valve.close()
            _LOGGER.info(
                "valve_close_response command response: %s", valve_close_response
            )

            # valve_halt_response = await guardian.valve.halt()
            # _LOGGER.info(
            #     "valve_halt_response command response: %s", valve_halt_response
            # )

            # valve_reset_response = await guardian.valve.reset()
            # _LOGGER.info(
            #     "valve_reset_response command response: %s", valve_reset_response
            # )
        except GuardianError as err:
            _LOGGER.info(err)


asyncio.run(main())
