from __future__ import annotations

from seadex._backup import BackupFile, SeaDexBackup
from seadex._entry import SeaDexEntry
from seadex._enums import Tracker
from seadex._exceptions import EntryNotFoundError, SeaDexException
from seadex._records import EntryRecord, TorrentRecord
from seadex._torrent import File, FileList, SeaDexTorrent

__version__ = "0.3.0"

__all__ = (
    "SeaDexEntry",
    # Torrent,
    "SeaDexTorrent",
    "File",
    "FileList",
    # Backup
    "SeaDexBackup",
    "BackupFile",
    # Records
    "EntryRecord",
    "TorrentRecord",
    # Enums
    "Tracker",
    # Exceptions
    "SeaDexException",
    "EntryNotFoundError",
    # Version
    "__version__",
)
