"""Define device info-related API endpoints."""
from typing import Callable

DEFAULT_FIRMWARE_UPGRADE_FILENAME = "latest.bin"
DEFAULT_FIRMWARE_UPGRADE_PORT = 443
DEFAULT_FIRMWARE_UPGRADE_URL = "https://repo.guardiancloud.services/gvc/fw"


class Device:
    """Define the endpoint manager.

    Note that this class shouldn't be instantiated directly; it will be instantiated as
    appropriate when creating a :meth:`aioguardian.client.Client`.
    """

    def __init__(self, execute_command: Callable) -> None:
        """Initialize."""
        self._execute_command = execute_command

    def diagnostics(self) -> dict:
        """Retrieve diagnostics info.

        :rtype: ``dict``
        """
        return self._execute_command(1)

    def factory_reset(self) -> dict:
        """Perform a factory reset on the device.

        :rtype: ``dict``
        """
        return self._execute_command(255)

    def ping(self) -> dict:
        """Ping the device.

        :rtype: ``dict``
        """
        return self._execute_command(0)

    def reboot(self) -> dict:
        """Reboot the device.

        :rtype: ``dict``
        """
        return self._execute_command(2)

    def upgrade_firmware(
        self,
        *,
        url: str = DEFAULT_FIRMWARE_UPGRADE_URL,
        port: int = DEFAULT_FIRMWARE_UPGRADE_PORT,
        filename: str = DEFAULT_FIRMWARE_UPGRADE_FILENAME
    ) -> dict:
        """Upgrade the firmware on the device.

        :param url: The firmware file's URL
        :type url: ``str``
        :param port: The firmware file's port
        :type url: ``int``
        :param filename: The firmware file's filename
        :type url: ``str``
        :rtype: ``dict``
        """
        return self._execute_command(
            4, params={"url": url, "port": port, "filename": filename}
        )
