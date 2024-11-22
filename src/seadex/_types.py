from __future__ import annotations

from datetime import datetime, timezone
from os import PathLike
from typing import Annotated, TypeAlias

from pydantic import AfterValidator

StrPath: TypeAlias = str | PathLike[str]
"""String or path-like objects"""

UTCDateTime: TypeAlias = Annotated[datetime, AfterValidator(lambda dt: dt.astimezone(timezone.utc))]
"""Datetime that's always in UTC."""
