"""Define common test utilities."""

from pathlib import Path


def load_fixture(filename: str) -> str:
    """Load a fixture.

    Args:
    ----
        filename: The filename of the fixtures/ file to load.

    Returns:
    -------
        A string containing the contents of the file.

    """
    path = Path(f"{Path(__file__).parent}/fixtures/{filename}")
    with Path.open(path, encoding="utf-8") as fptr:
        return fptr.read()
