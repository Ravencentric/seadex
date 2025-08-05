from __future__ import annotations

from typing import TYPE_CHECKING

from seadex._backup import BackupFile, SeaDexBackup
from seadex._entry import SeaDexEntry
from seadex._enums import Tag, Tracker
from seadex._exceptions import BadBackupFileError, EntryNotFoundError, SeaDexError
from seadex._torrent import SeaDexTorrent
from seadex._types import EntryRecord, File, TorrentRecord
from seadex._version import __version__

if TYPE_CHECKING:
    from collections.abc import Iterator


def entries() -> Iterator[EntryRecord]:  # pragma: no cover
    """
    Lazily iterate over all the entries in SeaDex.

    This function is a simple shortcut for a common idiom. For more
    control over the request or other means of retrieving entries, use the
    [`SeaDexEntry`][seadex.SeaDexEntry] class directly.
    """
    with SeaDexEntry() as seadex_entry:
        yield from seadex_entry.iterator()


__all__ = (
    "BackupFile",
    "BadBackupFileError",
    "EntryNotFoundError",
    "EntryRecord",
    "File",
    "SeaDexBackup",
    "SeaDexEntry",
    "SeaDexError",
    "SeaDexTorrent",
    "Tag",
    "TorrentRecord",
    "Tracker",
    "__version__",
    "entries",
)
