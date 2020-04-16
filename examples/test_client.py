"""Run an example script to quickly test the guardian."""
import asyncio
import logging

from aioguardian import Client
from aioguardian.errors import GuardianError

_LOGGER = logging.getLogger(__name__)


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.DEBUG)

    async with Client("172.16.11.208") as guardian:
        try:
            # Run through various device-related commands:
            ping_response = await guardian.device.ping()
            _LOGGER.info("Ping response: %s", ping_response)

            diagnostics_response = await guardian.device.diagnostics()
            _LOGGER.info("Diagnostics response: %s", diagnostics_response)

            reboot_response = await guardian.device.reboot()
            _LOGGER.info("Reboot response: %s", reboot_response)

            # factory_reset_response = await guardian.device.factory_reset()
            # _LOGGER.info("Factory reset response: %s", factory_reset_response)

            # upgrade_firmware_response = await guardian.device.upgrade_firmware()
            # _LOGGER.info("Upgrade firmware response: %s", upgrade_firmware_response)
        except GuardianError as err:
            _LOGGER.info(err)


asyncio.run(main())
