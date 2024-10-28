from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import Response


class SeaDexException(Exception):
    """Base Exception for all SeaDex related errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class EntryNotFoundError(SeaDexException):
    """The requested Entry was not found in SeaDex."""

    def __init__(self, message: str, *, response: Response) -> None:
        self.response = response
        super().__init__(message)
