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
            # --- DEVICE COMMANDS ---
            ping_response = await guardian.device.ping()
            _LOGGER.info("ping command response: %s", ping_response)

            diagnostics_response = await guardian.device.diagnostics()
            _LOGGER.info("diagnostics command response: %s", diagnostics_response)

            # reboot_response = await guardian.device.reboot()
            # _LOGGER.info("reboot command response: %s", reboot_response)

            # factory_reset_response = await guardian.device.factory_reset()
            # _LOGGER.info("factory_reset command response: %s", factory_reset_response)

            # upgrade_firmware_response = await guardian.device.upgrade_firmware()
            # _LOGGER.info(
            #     "upgrade_firmware command response: %s", upgrade_firmware_response
            # )

            # --- SENSOR COMMANDS ---
            sensor_status_response = await guardian.sensor.sensor_status()
            _LOGGER.info(
                "sensor_status_response command response: %s", sensor_status_response
            )

            # --- VALVE COMMANDS ---
            valve_status_response = await guardian.valve.valve_status()
            _LOGGER.info(
                "valve_status_response command response: %s", valve_status_response
            )

            valve_open_response = await guardian.valve.valve_open()
            _LOGGER.info(
                "valve_open_response command response: %s", valve_open_response
            )

            # Give the valve a chance to open fully so that the valve_close command
            # doesn't error out:
            await asyncio.sleep(3)

            valve_close_response = await guardian.valve.valve_close()
            _LOGGER.info(
                "valve_close_response command response: %s", valve_close_response
            )
        except GuardianError as err:
            _LOGGER.info(err)


asyncio.run(main())
