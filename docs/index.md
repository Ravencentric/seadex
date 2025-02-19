<br/>
<p align="center">
  <a href="https://github.com/Ravencentric/seadex">
    <img src="https://raw.githubusercontent.com/Ravencentric/seadex/refs/heads/main/docs/assets/logo.png" alt="Logo" width="200">
  </a>
  <p align="center">
    Python wrapper for the SeaDex API
  </p>
</p>

<p align="center">
<a href="https://pypi.org/project/seadex/"><img src="https://img.shields.io/pypi/v/seadex" alt="PyPI - Version" ></a>
<img src="https://img.shields.io/pypi/pyversions/seadex" alt="PyPI - Python Version">
<img src="https://img.shields.io/github/license/Ravencentric/seadex" alt="License">
<img src="https://img.shields.io/pypi/types/seadex" alt="PyPI - Types">
</p>

<p align="center">
<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/seadex/release.yml?" alt="GitHub Workflow Status">
<img src="https://img.shields.io/github/actions/workflow/status/Ravencentric/seadex/tests.yml?label=tests" alt="GitHub Workflow Status">
<a href="https://codecov.io/gh/Ravencentric/seadex"><img src="https://codecov.io/gh/Ravencentric/seadex/graph/badge.svg?token=B45ODO7TEY" alt="Codecov"></a>
</p>

## Table Of Contents

* [About](#about)
* [Installation](#installation)
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

## License

Distributed under the [MIT](https://choosealicense.com/licenses/mit/) License. See [LICENSE](https://github.com/Ravencentric/seadex/blob/main/LICENSE) for more information.
