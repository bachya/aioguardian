Supported Commands
==================

``aioguardian`` supports the following commands:

* :meth:`client.device.diagnostics() <aioguardian.commands.device.Device.diagnostics>`: return diagnostics info from the device
* :meth:`client.device.factory_reset() <aioguardian.commands.device.Device.factory_reset>`: perform a factory reset of the device
* :meth:`client.device.ping() <aioguardian.commands.device.Device.ping>`: ping the device to determine whether it can be reached
* :meth:`client.device.publish_state() <aioguardian.commands.device.Device.publish_state>`: publish the device state to the Guardian cloud
* :meth:`client.device.reboot() <aioguardian.commands.device.Device.reboot>`: reboot the device
* :meth:`client.device.upgrade_firmware() <aioguardian.commands.device.Device.upgrade_firmware>`: initiate a firmware upgrade on the device
* :meth:`client.device.wifi_configure() <aioguardian.commands.device.Device.wifi_configure>`: connect the device to an SSID
* :meth:`client.device.wifi_disable_ap() <aioguardian.commands.device.Device.wifi_disable_ap>`: disable the device's onboard WiFi access point
* :meth:`client.device.wifi_enable_ap() <aioguardian.commands.device.Device.wifi_enable_ap>`: enable the device's onboard WiFi access point
* :meth:`client.device.wifi_reset() <aioguardian.commands.device.Device.wifi_reset>`: reset all WiFi info
* :meth:`client.device.wifi_status() <aioguardian.commands.device.Device.wifi_status>`: get information related to the device's WiFi connections
* :meth:`client.sensor.pair_dump() <aioguardian.commands.sensor.Sensor.pair_dump>`: get information on all paired sensors
* :meth:`client.sensor.pair_sensor() <aioguardian.commands.sensor.Sensor.pair_sensor>`: pair a new sensor to the device
* :meth:`client.sensor.sensor_status() <aioguardian.commands.sensor.Sensor.sensor_status>`: get information from the device's onboard sensors
* :meth:`client.valve.valve_close() <aioguardian.commands.valve.Valve.close>`: close the valve
* :meth:`client.valve.valve_halt() <aioguardian.commands.valve.Valve.halt>`: halt the valve mid-open or mid-close (be careful!)
* :meth:`client.valve.valve_open() <aioguardian.commands.valve.Valve.open>`: open the valve
* :meth:`client.valve.valve_reset() <aioguardian.commands.valve.Valve.reset>`: reset all valve diagnostics
* :meth:`client.valve.valve_status() <aioguardian.commands.valve.Valve.valve_status>`: get information about the device's valve
