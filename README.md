# 🚰 aioguardian: A Python3 library for Elexa Guardian devices

[![CI](https://github.com/bachya/aioguardian/workflows/CI/badge.svg)](https://github.com/bachya/aioguardian/actions)
[![PyPi](https://img.shields.io/pypi/v/aioguardian.svg)](https://pypi.python.org/pypi/aioguardian)
[![Version](https://img.shields.io/pypi/pyversions/aioguardian.svg)](https://pypi.python.org/pypi/aioguardian)
[![License](https://img.shields.io/pypi/l/aioguardian.svg)](https://github.com/bachya/aioguardian/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/aioguardian/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/aioguardian)
[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/aioguardian/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`aioguardian` is a Python3, `asyncio`-focused library for interacting with
[the Guardian line of water valves and sensors from Elexa](http://getguardian.com).

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Usage](#usage)
- [Commands](#commands)
- [Contributing](#contributing)

# Installation

```python
pip install aioguardian
```

# Python Versions

`aioguardian` is currently supported on:

* Python 3.6
* Python 3.7
* Python 3.8 

# Usage

```python
import asyncio

from aioguardian import Client
from aioguardian.errors import GuardianError


async with Client("192.168.1.100") as client:
    # Run various commands:
    await client.device.ping()
    await client.device.diagnostics()


asyncio.run(main())
```

If the mood should strike you, you can manually instantiate a `Client` object and manage
connection to and disconnection from the device yourself:

```python
import asyncio

from aioguardian import Client
from aioguardian.errors import GuardianError


# Create a client with the IP address or hostname of your Guardian device:
client = Client("192.168.1.100")

# Connect to the device:
await client.connect()

# Run various commands:
await client.device.ping()
await client.device.diagnostics()

# Disconnect from the device – notice that this is a regular method:
client.disconnect()


asyncio.run(main())
```
## Commands

Many commands are available:

* `client.device.diagnostics()`: return diagnostics info from the device
* `client.device.factory_reset()`: perform a factory reset of the device
* `client.device.ping()`: ping the device to determine whether it can be reached
* `client.device.reboot()`: reboot the device
* `client.device.upgrade_firmware()`: initiate a firmware upgrade on the device
* `client.sensor.sensor_status()`: get information from the device's onboard sensors
* `client.valve.valve_close()`: close the valve
* `client.valve.valve_halt()`: halt the valve mid-open or mid-close (be careful!)
* `client.valve.valve_open()`: open the valve
* `client.valve.valve_status()`: get information about the device's valve
* `client.valve.valve_reset()`: reset all valve diagnostics

Details on how to use each operation can be found in the docstrings for the various
methods; similarly, the test fixtures demonstrate the various types of JSON responses
you can anticipate.

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/aioguardian/issues)
  or [initiate a discussion on one](https://github.com/bachya/aioguardian/issues/new).
2. [Fork the repository](https://github.com/bachya/aioguardian/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `script/test`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
