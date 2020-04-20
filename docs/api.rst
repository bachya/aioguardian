API Reference
=============

.. toctree::
   :maxdepth: 3

.. module:: aioguardian

Client
------

.. autoclass:: Client
   :members:

Command Classes
---------------

The classes should not be instantiated directly; rather, they exist as properties of a
:meth:`aioguardian.Client` class:

* ``client.device`` is an instance of :meth:`aioguardian.commands.device.Device`.
* ``client.sensor`` is an instance of :meth:`aioguardian.commands.sensor.Sensor`.
* ``client.valve`` is an instance of :meth:`aioguardian.commands.valve.Valve`.

Device
******

.. autoclass:: aioguardian.commands.device.Device
   :members:

Sensor
******

.. autoclass:: aioguardian.commands.sensor.Sensor
   :members:

Valve
*****

.. autoclass:: aioguardian.commands.valve.Valve
   :members:

Errors
------

.. automodule:: aioguardian.errors
   :members:
