API Reference
=============

.. toctree::
   :maxdepth: 3

.. module:: aioguardian

Client
------

.. autoclass:: Client
   :members:

Command Helpers
---------------

.. automodule:: aioguardian.helpers.command
   :members:
   :undoc-members:

Command Classes
---------------

The classes should not be instantiated directly; rather, they exist as properties of a
:meth:`aioguardian.Client` class:

* ``client.iot`` is an instance of :meth:`aioguardian.commands.iot.IOTCommands`.
* ``client.system`` is an instance of :meth:`aioguardian.commands.system.SystemCommands`.
* ``client.sensor`` is an instance of :meth:`aioguardian.commands.sensor.SensorCommands`.
* ``client.valve`` is an instance of :meth:`aioguardian.commands.valve.ValveCommands`.
* ``client.wifi`` is an instance of :meth:`aioguardian.commands.wifi.WiFiCommands`.

IOT
***

.. autoclass:: aioguardian.commands.iot.IOTCommands
   :members:

Sensor
******

.. autoclass:: aioguardian.commands.sensor.SensorCommands
   :members:

System
******

.. autoclass:: aioguardian.commands.system.SystemCommands
   :members:

Valve
*****

.. autoclass:: aioguardian.commands.valve.ValveCommands
   :members:

WiFi
****

.. autoclass:: aioguardian.commands.wifi.WiFiCommands
   :members:

Errors
------

.. automodule:: aioguardian.errors
   :members:
