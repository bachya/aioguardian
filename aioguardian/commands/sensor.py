"""async define onboard sensor-related API endpoints."""
from typing import Callable, Coroutine

import voluptuous as vol

from aioguardian.errors import CommandError
from aioguardian.helpers.command import Command
import aioguardian.helpers.config_validation as cv

PARAM_UID = "uid"

PAIR_SENSOR_PARAM_SCHEMA: vol.Schema = vol.Schema(
    {vol.Required(PARAM_UID): vol.All(cv.alphanumeric, vol.Length(max=12))}
)


class Sensor:
    """Define an object to manage sensor-related commands.

    Note that this class shouldn't be instantiated directly; an instance of it will
    automatically be added to the :meth:`Client <aioguardian.Client>` (as
    ``client.sensor``).
    """

    def __init__(self, execute_command: Callable[..., Coroutine]) -> None:
        """Initialize."""
        self._execute_command: Callable[..., Coroutine] = execute_command

    async def pair_dump(self, *, silent: bool = True) -> dict:
        """Dump information on all paired sensors.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.pair_dump, silent=silent)

    async def pair_sensor(self, uid: str, *, silent: bool = True) -> dict:
        """Pair a new sensor to the device.

        :param uid: The UID of the sensor to pair
        :type uid: ``str``
        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        params = {PARAM_UID: uid}

        try:
            PAIR_SENSOR_PARAM_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        return await self._execute_command(
            Command.pair_sensor, params=params, silent=silent
        )

    async def vc_sensor_status(self, *, silent: bool = True) -> dict:
        """Retrieve status of the valve controller sensors.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        return await self._execute_command(Command.vc_sensor_status, silent=silent)
