Commands
========

``aioguardian`` supports all of the commands provided by the official Guardian API.

Supported Commands
------------------

* :meth:`client.iot.publish_state() <aioguardian.commands.iot.IOTCommands.publish_state>`: publish the device state to the Guardian cloud
* :meth:`client.sensor.pair_dump() <aioguardian.commands.sensor.SensorCommands.pair_dump>`: dump the UIDs of all paired sensors
* :meth:`client.sensor.pair_sensor() <aioguardian.commands.sensor.SensorCommands.pair_sensor>`: pair a new sensor to the device
* :meth:`client.sensor.paired_sensor_status() <aioguardian.commands.sensor.SensorCommands.paired_sensor_status>`: get information from a paired sensor
* :meth:`client.sensor.unpair_sensor() <aioguardian.commands.sensor.SensorCommands.unpair_sensor>`: unpair a sensor from the device
* :meth:`client.system.diagnostics() <aioguardian.commands.system.SystemCommands.diagnostics>`: return diagnostics info from the device
* :meth:`client.system.factory_reset() <aioguardian.commands.system.SystemCommands.factory_reset>`: perform a factory reset of the device
* :meth:`client.system.onboard_sensor_status() <aioguardian.commands.system.SystemCommands.onboard_sensor_status>`: get information from the device's onboard sensors
* :meth:`client.system.ping() <aioguardian.commands.system.SystemCommands.ping>`: ping the device to determine whether it can be reached
* :meth:`client.system.reboot() <aioguardian.commands.system.SystemCommands.reboot>`: reboot the device
* :meth:`client.system.upgrade_firmware() <aioguardian.commands.system.SystemCommands.upgrade_firmware>`: initiate a firmware upgrade on the device
* :meth:`client.valve.close() <aioguardian.commands.valve.ValveCommands.close>`: close the valve
* :meth:`client.valve.halt() <aioguardian.commands.valve.ValveCommands.halt>`: halt the valve mid-open or mid-close (be careful!)
* :meth:`client.valve.open() <aioguardian.commands.valve.ValveCommands.open>`: open the valve
* :meth:`client.valve.reset() <aioguardian.commands.valve.ValveCommands.reset>`: reset all valve diagnostics
* :meth:`client.valve.status() <aioguardian.commands.valve.ValveCommands.status>`: get information about the device's valve
* :meth:`client.wifi.configure() <aioguardian.commands.wifi.WiFiCommands.configure>`: connect the device to an SSID
* :meth:`client.wifi.disable_ap() <aioguardian.commands.wifi.WiFiCommands.disable_ap>`: disable the device's onboard WiFi access point
* :meth:`client.wifi.enable_ap() <aioguardian.commands.wifi.WiFiCommands.enable_ap>`: enable the device's onboard WiFi access point
* :meth:`client.wifi.list() <aioguardian.commands.wifi.WiFiCommands.list>`: list nearby WiFi SSIDs
* :meth:`client.wifi.reset() <aioguardian.commands.wifi.WiFiCommands.reset>`: reset all WiFi info
* :meth:`client.wifi.scan() <aioguardian.commands.wifi.WiFiCommands.scan>`: scan for nearby WiFi SSIDs
* :meth:`client.wifi.status() <aioguardian.commands.wifi.WiFiCommands.status>`: get information related to the device's WiFi connections

*Note:* Not all commands are supported on all firmwares. If a particular command is not working on your valve controller, please ensure you have the latest device firmware before filing an ``aioguardian`` bug.

You can learn more about the response payloads of these commands by looking at the
`fixtures folder <https://github.com/bachya/aioguardian/tree/dev/tests/fixtures>`_
in the GitHub repo.

Executing Raw Commands
----------------------

If you should ever need to quickly test commands via their integer command code, the
:meth:`Client <aioguardian.Client>` object's
:meth:`execute_raw_command() <aioguardian.Client.execute_raw_command>` can be
used:

.. code:: python

  import asyncio

    from aioguardian import Client


    async def main():
        async with Client("<IP ADDRESS>") as client:
            # Get sensor status, which is command 80:
            status = await client.execute_raw_command(80)


    asyncio.run(main())


You can see the command-code-to-command mapping by examining the
:meth:`Command <aioguardian.helpers.command.Command>` helper.


Dealing with "Beeps"
--------------------

Under normal operation, the device will emit a series of "beep" tones alongside certain
actions. As this can be a bit much, by default, ``aioguardian`` suppresses these tones
for commands that don't affect the valve's status. Should this behavior not be
desirable, many command methods accept a ``silent`` argument.

For example, to execute
:meth:`client.system.ping() <aioguardian.commands.system.SystemCommands.ping>` and allow these
tones to play:

.. code:: python

  import asyncio

    from aioguardian import Client


    async def main():
        async with Client("<IP ADDRESS>") as client:
            await client.system.ping(silent=False)


    asyncio.run(main())
