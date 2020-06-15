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

            # publish_state_response = await guardian.device.publish_state()
            # _LOGGER.info("publish_state command response: %s", publish_state_response)

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

            wifi_status_response = await guardian.wifi.status()
            _LOGGER.info("wifi_status command response: %s", wifi_status_response)

            # wifi_reset_response = await guardian.wifi.reset()
            # _LOGGER.info("wifi_reset command response: %s", wifi_reset_response)

            # wifi_configure_response = await guardian.wifi.configure(
            #     "<SSID>", "<PASSWORD>"
            # )
            # _LOGGER.info("wifi_configure command response: %s", wifi_configure_response)

            # wifi_enable_ap_response = await guardian.wifi.enable_ap()
            # _LOGGER.info("wifi_enable_ap command response: %s", wifi_enable_ap_response)

            # wifi_disable_ap_response = await guardian.wifi.disable_ap()
            # _LOGGER.info(
            #     "wifi_disable_ap command response: %s", wifi_disable_ap_response
            # )

            # --- SENSOR COMMANDS ---
            onboard_sensor_status = await guardian.sensor.onboard_sensor_status()
            _LOGGER.info(
                "onboard_sensor_status command response: %s", onboard_sensor_status
            )

            pair_dump_response = await guardian.sensor.pair_dump()
            _LOGGER.info("pair_dump_response command response: %s", pair_dump_response)

            # pair_sensor_response = await guardian.sensor.pair_sensor("<UID>")
            # _LOGGER.info("pair_response command response: %s", pair_sensor_response)

            # --- VALVE COMMANDS ---
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
