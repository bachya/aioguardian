"""Run an example script to quickly test the async client."""
import asyncio
import logging
import time

from aioguardian import Client
from aioguardian.errors import GuardianError

_LOGGER = logging.getLogger(__name__)


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.DEBUG)

    client = Client("172.16.11.208", use_async=True)

    start = time.time()

    try:
        # Run through various device-related commands:
        ping_response = await client.device.ping()
        _LOGGER.info("Ping response: %s", ping_response)

        diagnostics_response = await client.device.diagnostics()
        _LOGGER.info("Diagnostics response: %s", diagnostics_response)

        reboot_response = await client.device.reboot()
        _LOGGER.info("Reboot response: %s", reboot_response)

        # factory_reset_response = await client.device.factory_reset()
        # _LOGGER.info("Factory reset response: %s", factory_reset_response)

        # upgrade_firmware_response = await client.device.upgrade_firmware()
        # _LOGGER.info("Upgrade firmware response: %s", upgrade_firmware_response)
    except GuardianError as err:
        _LOGGER.info(err)

    end = time.time()

    _LOGGER.info("Execution time: %s seconds", end - start)


asyncio.get_event_loop().run_until_complete(main())
