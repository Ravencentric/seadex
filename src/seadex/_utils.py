from __future__ import annotations

from pathlib import Path

from seadex._types import StrPath


def realpath(path: StrPath) -> Path:
    """
    Resolve Path or Path-like strings and return a Path object.
    """
    return Path(path).expanduser().resolve()
