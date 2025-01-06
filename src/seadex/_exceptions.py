from __future__ import annotations


class SeaDexError(Exception):
    """Base Exception for all SeaDex related errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class EntryNotFoundError(SeaDexError):
    """The requested Entry was not found in SeaDex."""


class BadBackupFileError(SeaDexError):
    """The backup file is broken."""
