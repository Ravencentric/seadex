from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import httpx

from seadex._version import __version__

if TYPE_CHECKING:
    from seadex._types import StrPath


def realpath(path: StrPath) -> Path:
    """
    Resolve Path or Path-like strings and return a Path object.
    """
    return Path(path).expanduser().resolve()


def httpx_client(*, timeout: httpx.Timeout | None = None) -> httpx.Client:
    """
    Return an instance of an httpx.Client.
    """
    headers = {"User-Agent": f"seadex/{__version__} (https://pypi.org/project/seadex/)"}

    if timeout is not None:
        return httpx.Client(headers=headers, timeout=timeout)
    return httpx.Client(headers=headers)
