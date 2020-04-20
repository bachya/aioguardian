Usage
=====


Installation
------------

.. code:: bash

   pip install aioguardian

Python Versions
---------------

``aioguardian`` is currently supported on:

* Python 3.6
* Python 3.7
* Python 3.8

Get Up and Running
------------------

Getting up and running with ``aioguardian`` is very simple! Merely create a
:meth:`Client <aioguardian.Client>` class with the IP address of the device and get to
work:

.. code:: python

  import asyncio

    from aioguardian import Client


    async def main():
        client = Client("<IP ADDRESS>")

        # Note that disconnection is accomplished via a coroutine:
        await client.connect()

        # ...run commands...

        # Note that disconnection is accomplished via a regular method:
        client.disconnect()


    asyncio.run(main())

If you would prefer, the :meth:`Client <aioguardian.Client>` class also comes with a
context manager that handles connection/disconnection for you:

.. code:: python

  import asyncio

    from aioguardian import Client


    async def main():
        async with Client("<IP ADDRESS>") as client:
            # ...run commands...


    asyncio.run(main())
