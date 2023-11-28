"""Define custom validators."""
from typing import Any, cast
from urllib.parse import urlparse

import voluptuous as vol


def alphanumeric(value: Any) -> str:
    """Validate that a string is alphanumeric only.

    Args:
        value: A value to evaluae.

    Returns:
        An alphanumeric string.

    Raises:
        Invalid: Raised when a non-alphanumeric string is encountered.
    """
    str_value = str(value)

    if str_value.isalnum():
        return str_value

    raise vol.Invalid("String is not alphanumeric")


def url(value: Any) -> str:
    """Validate that a string is a URL.

    Args:
        value: A value to evaluae.

    Returns:
        An URL string.

    Raises:
        Invalid: Raised when a non-URL string is encountered.
    """
    url_in = str(value)

    if urlparse(url_in).scheme in ["http", "https"]:
        return cast(
            str,
            vol.Schema(vol.Url())(url_in),  # pylint: disable=no-value-for-parameter
        )

    raise vol.Invalid("Invalid URL")
