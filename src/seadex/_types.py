from __future__ import annotations

from os import PathLike
from typing import TYPE_CHECKING, Any, TypeAlias

import msgspec

if TYPE_CHECKING:
    from typing_extensions import Self


StrPath: TypeAlias = str | PathLike[str]
"""String or path-like objects"""


class Base(
    msgspec.Struct,
    forbid_unknown_fields=True,
    repr_omit_defaults=True,
    frozen=True,
    kw_only=True,
):
    """Base class for AniList data structures."""

    @classmethod
    def from_dict(cls, data: dict[str, Any], /) -> Self:
        """
        Create an instance of this class from a dictionary.

        Parameters
        ----------
        data : dict[str, Any]
            Dictionary representing the instance of this class.

        Returns
        -------
        Self
            An instance of this class.

        """
        return msgspec.convert(data, type=cls)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the instance of this class into a dictionary.

        Returns
        -------
        dict[str, Any]
            Dictionary representing the instance of this class.

        """
        return msgspec.to_builtins(self)  # type: ignore[no-any-return]

    @classmethod
    def from_json(cls, data: str | bytes, /) -> Self:
        """
        Create an instance of this class from JSON data.

        Parameters
        ----------
        data : str | bytes
            JSON data representing the instance of this class.

        Returns
        -------
        Self
            An instance of this class.

        """
        return msgspec.json.decode(data, type=cls)

    def to_json(self, *, indent: int = 2) -> str:
        """
        Serialize the instance of this class into a JSON string.

        Parameters
        ----------
        indent : int, optional
            Number of spaces for indentation.
            Set to 0 for a single line with spacing,
            or negative to minimize size by removing extra whitespace.

        Returns
        -------
        str
            JSON string representing this class.

        """
        jsonified = msgspec.json.encode(self)
        return msgspec.json.format(jsonified, indent=indent).decode()


class File(Base, frozen=True, kw_only=True):
    """Represents a file in the torrent."""

    name: str
    """The name of the file."""
    size: int
    """The size of the file in bytes."""

    def __str__(self) -> str:
        """Implement the string representation. Equivalent to `File.name`."""
        return self.name
