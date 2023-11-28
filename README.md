# 🚰 aioguardian: A Python3 library for Elexa Guardian devices

[![CI][ci-badge]][ci]
[![PyPI][pypi-badge]][pypi]
[![Version][version-badge]][version]
[![License][license-badge]][license]
[![Code Coverage][codecov-badge]][codecov]
[![Maintainability][maintainability-badge]][maintainability]

<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

`aioguardian` is a Python3, `asyncio`-focused library for interacting with
[the Guardian line of water valves and sensors from Elexa][elexa].

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Documentation](#documentation)
- [Contributing](#contributing)

# Installation

```bash
pip install aioguardian
```

# Python Versions

`aioguardian` is currently supported on:

- Python 3.10
- Python 3.11
- Python 3.12

# Documentation

Complete documentation can be found [here][docs].

# Contributing

Thanks to all of [our contributors][contributors] so far!

1. [Check for open features/bugs][issues] or [initiate a discussion on one][new-issue].
2. [Fork the repository][fork].
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix on a new branch.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `poetry run pytest --cov aioguardian tests`
9. Update `README.md` with any new documentation.
10. Submit a pull request!

[ci-badge]: https://github.com/bachya/aioguardian/workflows/CI/badge.svg
[ci]: https://github.com/bachya/aioguardian/actions
[codecov-badge]: https://codecov.io/gh/bachya/aioguardian/branch/dev/graph/badge.svg
[codecov]: https://codecov.io/gh/bachya/aioguardian
[contributors]: https://github.com/bachya/aioguardian/graphs/contributors
[docs]: http://aioguardian.readthedocs.io
[elexa]: http://getguardian.com
[fork]: https://github.com/bachya/aioguardian/fork
[issues]: https://github.com/bachya/aioguardian/issues
[license-badge]: https://img.shields.io/pypi/l/aioguardian.svg
[license]: https://github.com/bachya/aioguardian/blob/main/LICENSE
[maintainability-badge]: https://api.codeclimate.com/v1/badges/e6521f4a50efd222be18/maintainability
[maintainability]: https://codeclimate.com/github/bachya/aioguardian/maintainability
[new-issue]: https://github.com/bachya/aioguardian/issues/new
[new-issue]: https://github.com/bachya/aioguardian/issues/new
[pypi-badge]: https://img.shields.io/pypi/v/aioguardian.svg
[pypi]: https://pypi.python.org/pypi/aioguardian
[version-badge]: https://img.shields.io/pypi/pyversions/aioguardian.svg
[version]: https://pypi.python.org/pypi/aioguardian
