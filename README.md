# 🚰 aioguardian: A Python3 library for Elexa Guardian devices

[![CI](https://github.com/bachya/aioguardian/workflows/CI/badge.svg)](https://github.com/bachya/aioguardian/actions)
[![PyPi](https://img.shields.io/pypi/v/aioguardian.svg)](https://pypi.python.org/pypi/aioguardian)
[![Version](https://img.shields.io/pypi/pyversions/aioguardian.svg)](https://pypi.python.org/pypi/aioguardian)
[![License](https://img.shields.io/pypi/l/aioguardian.svg)](https://github.com/bachya/aioguardian/blob/main/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/aioguardian/branch/dev/graph/badge.svg)](https://codecov.io/gh/bachya/aioguardian)
[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/aioguardian/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

`aioguardian` is a Python3, `asyncio`-focused library for interacting with
[the Guardian line of water valves and sensors from Elexa](http://getguardian.com).

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

- Python 3.9
- Python 3.10
- Python 3.11

# Documentation

Complete documentation can be found here: http://aioguardian.readthedocs.io

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/aioguardian/issues)
   or [initiate a discussion on one](https://github.com/bachya/aioguardian/issues/new).
2. [Fork the repository](https://github.com/bachya/aioguardian/fork).
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `poetry run pytest --cov aioguardian tests`
9. Update `README.md` with any new documentation.
10. Add yourself to `AUTHORS.md`.
11. Submit a pull request!
