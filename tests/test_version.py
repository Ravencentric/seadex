from __future__ import annotations

import tomli

from seadex._version import __version__


def test_versions_match() -> None:
    with open("pyproject.toml", "rb") as f:
        pyproject_version = tomli.load(f)["project"]["version"]
    assert pyproject_version == __version__
