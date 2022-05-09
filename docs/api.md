# API Reference

```{toctree}
:maxdepth: 3
```

```{eval-rst}
.. module:: aioguardian
```

## Client

```{eval-rst}
.. autoclass:: Client
   :members:
```

## Command Helpers

```{eval-rst}
.. automodule:: aioguardian.helpers.command
   :members:
   :undoc-members:
```

## Command Classes

The classes should not be instantiated directly; rather, they exist as properties of a
{meth}`aioguardian.Client` class:

- `client.iot` is an instance of {meth}`aioguardian.commands.iot.IOTCommands`.
- `client.system` is an instance of {meth}`aioguardian.commands.system.SystemCommands`.
- `client.sensor` is an instance of {meth}`aioguardian.commands.sensor.SensorCommands`.
- `client.valve` is an instance of {meth}`aioguardian.commands.valve.ValveCommands`.
- `client.wifi` is an instance of {meth}`aioguardian.commands.wifi.WiFiCommands`.

### IOT

```{eval-rst}
.. autoclass:: aioguardian.commands.iot.IOTCommands
   :members:
```

### Sensor

```{eval-rst}
.. autoclass:: aioguardian.commands.sensor.SensorCommands
   :members:
```

### System

```{eval-rst}
.. autoclass:: aioguardian.commands.system.SystemCommands
   :members:
```

### Valve

```{eval-rst}
.. autoclass:: aioguardian.commands.valve.ValveCommands
   :members:
```

### WiFi

```{eval-rst}
.. autoclass:: aioguardian.commands.wifi.WiFiCommands
   :members:
```

## Errors

```{eval-rst}
.. automodule:: aioguardian.errors
   :members:
```
