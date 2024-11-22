from __future__ import annotations

from pathlib import Path

from httpx import Client

from seadex import __version__
from seadex._types import StrPath


def realpath(path: StrPath) -> Path:
    """
    Resolve Path or Path-like strings and return a Path object.
    """
    return Path(path).expanduser().resolve()


def httpx_client() -> Client:
    """
    Default HTTPX client.
    """
    return Client(headers={"user-agent": f"seadex/{__version__}"})
