from __future__ import annotations

from importlib import metadata
from typing import NamedTuple


class Version(NamedTuple):
    major: int
    minor: int
    micro: int


__version__ = metadata.version("seadex")
__version_tuple__ = Version(*[int(i) for i in __version__.split(".")])
