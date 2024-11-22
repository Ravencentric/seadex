from __future__ import annotations

from pathlib import Path

from httpx import Client

from seadex._types import StrPath
from seadex._version import __version__


def realpath(path: StrPath) -> Path:
    """
    Resolve Path or Path-like strings and return a Path object.
    """
    return Path(path).expanduser().resolve()


def httpx_client() -> Client:
    """
    Return an instance of an httpx.Client.
    """
    return Client(headers={"user-agent": f"seadex/{__version__}"})
