<br/>
<p align="center">
  <a href="https://github.com/Ravencentric/seadex">
    <img src="https://raw.githubusercontent.com/Ravencentric/seadex/refs/heads/main/docs/assets/logo.png" alt="Logo" width="200">
  </a>
  <p align="center">
    Python wrapper for the SeaDex API.
  </p>
</p>

<div align="center">

[![PyPI - Version](https://img.shields.io/pypi/v/seadex?link=https%3A%2F%2Fpypi.org%2Fproject%2Fseadex%2F)](https://pypi.org/project/seadex/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/seadex)
![License](https://img.shields.io/github/license/Ravencentric/seadex)
![PyPI - Types](https://img.shields.io/pypi/types/seadex)

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Ravencentric/seadex/release.yml)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ravencentric/seadex/tests.yml?label=tests)
[![codecov](https://codecov.io/gh/Ravencentric/seadex/graph/badge.svg?token=B45ODO7TEY)](https://codecov.io/gh/Ravencentric/seadex)

</div>

## Table Of Contents

* [About](#about)
* [Installation](#installation)
* [Docs](#docs)
* [License](#license)

## About

Python wrapper for the [SeaDex API](https://releases.moe/about/).

## Installation

`seadex` is available on [PyPI](https://pypi.org/project/seadex/), and can be installed using [pip](https://pip.pypa.io/en/stable/installation/).

1. To install the core library:

    ```sh
    pip install seadex
    ```

2. To install with the CLI tools:

    - With [`pipx`](https://pipx.pypa.io/stable/) or [`uv`](https://docs.astral.sh/uv/guides/tools/#installing-tools) (recommended)

        ```sh
        pipx install "seadex[cli]"
        ```
        ```sh
        uv tool install "seadex[cli]"
        ```

    - With [`pip`](https://pip.pypa.io/en/stable/installation/)

        ```sh
        pip install "seadex[cli]"
        ```

## Docs

Checkout the complete documentation [here](https://seadex.ravencentric.cc/).

## License

Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License. See [LICENSE](https://github.com/Ravencentric/seadex/blob/main/LICENSE) for more information.
