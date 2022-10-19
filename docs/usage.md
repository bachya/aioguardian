# Usage

## Installation

```bash
pip install aioguardian
```

## Python Versions

`aioguardian` is currently supported on:

- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11

## Get Up and Running

Getting up and running with `aioguardian` is very simple! Merely create a
{meth}`Client <aioguardian.Client>` class with the IP address of the device and get to
work:

```python
import asyncio

  from aioguardian import Client


  async def main():
      client = Client("<IP ADDRESS>")

      # Note that connecting to the Guardian is accomplished via a coroutine:
      await client.connect()

      # ...run commands...

      # Note that disconnecting from the Guardian is accomplished via a regular method:
      client.disconnect()


  asyncio.run(main())
```

If you would prefer, the {meth}`Client <aioguardian.Client>` class also comes with a
context manager that handles connection/disconnection for you:

```python
import asyncio

  from aioguardian import Client


  async def main():
      async with Client("<IP ADDRESS>") as client:
          # ...run commands...


  asyncio.run(main())
```
