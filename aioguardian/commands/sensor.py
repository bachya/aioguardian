"""Define sensor commands."""
from typing import Any, Awaitable, Callable, Dict, cast

import voluptuous as vol

from aioguardian.errors import CommandError
from aioguardian.helpers.command import Command
import aioguardian.helpers.config_validation as cv

PARAM_UID = "uid"

PAIRED_SENSOR_UID_SCHEMA: vol.Schema = vol.Schema(
    {vol.Required(PARAM_UID): vol.All(cv.alphanumeric, vol.Length(max=12))}
)


class SensorCommands:
    """Define an object to manage sensor commands.

    Note that this class shouldn't be instantiated directly; an instance of it will
    automatically be added to the :meth:`Client <aioguardian.Client>` (as
    ``client.sensor``).
    """

    def __init__(self, execute_command: Callable[..., Awaitable]) -> None:
        """Initialize."""
        self._execute_command = execute_command

    async def pair_dump(self, *, silent: bool = True) -> Dict[str, Any]:
        """Dump information on all paired sensors.

        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        data = await self._execute_command(Command.sensor_pair_dump, silent=silent)
        return cast(Dict[str, Any], data)

    async def pair_sensor(self, uid: str, *, silent: bool = True) -> Dict[str, Any]:
        """Pair a new sensor to the device.

        :param uid: The UID of the sensor to pair
        :type uid: ``str``
        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        params = {PARAM_UID: uid}

        try:
            PAIRED_SENSOR_UID_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        data = await self._execute_command(
            Command.sensor_pair_sensor, params=params, silent=silent
        )
        return cast(Dict[str, Any], data)

    async def paired_sensor_status(
        self, uid: str, *, silent: bool = True
    ) -> Dict[str, Any]:
        """Get the status (leak, temperature, etc.) of a paired sensor.

        :param uid: The UID of the sensor to pair
        :type uid: ``str``
        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        params = {PARAM_UID: uid}

        try:
            PAIRED_SENSOR_UID_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        data = await self._execute_command(
            Command.sensor_paired_sensor_status, params=params, silent=silent
        )
        return cast(Dict[str, Any], data)

    async def unpair_sensor(self, uid: str, *, silent: bool = True) -> Dict[str, Any]:
        """Unpair a sensor from the device.

        :param uid: The UID of the sensor to unpair
        :type uid: ``str``
        :param silent: If ``True``, silence "beep" tones associated with this command
        :type silent: ``bool``
        :rtype: ``dict``
        """
        params = {PARAM_UID: uid}

        try:
            PAIRED_SENSOR_UID_SCHEMA(params)
        except vol.Invalid as err:
            raise CommandError(f"Invalid parameters provided: {err}") from None

        data = await self._execute_command(
            Command.sensor_unpair_sensor, params=params, silent=silent
        )
        return cast(Dict[str, Any], data)
