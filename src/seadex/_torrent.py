from __future__ import annotations

import json
from functools import cached_property
from os.path import basename
from pathlib import Path

from pydantic import ByteSize, field_validator
from torf import Torrent as TorfTorrent

from seadex._models import FrozenBaseModel
from seadex._types import StrPath
from seadex._utils import realpath


class File(FrozenBaseModel):
    """Represents a file in the torrent."""

    name: str
    """The name of the file."""
    size: ByteSize
    """The size of the file in bytes."""

    def __str__(self) -> str:
        """Stringify, equivalent to [`File.name`][File.name]."""
        return self.name

    def __fspath__(self) -> str:
        """Path representation, equivalent to [`File.name`][File.name]."""
        return self.name

    @field_validator("name", mode="before")
    @classmethod
    def _as_posix(cls, v: str) -> str:
        """Ensure the names are posix compatible."""
        return Path(v).as_posix()


class FileList(tuple[File, ...]):
    """A tuple-based collection of `File` objects."""

    def to_json(self, indent: int | None = None) -> str:
        """
        Convert the file list to a JSON string that's compatible with SeaDex.

        Parameters
        ----------
        indent : int | None, optional
            Number of spaces for indentation in the output JSON string.

        Returns
        -------
        str
            The file list in JSON format.

        """
        files = []

        for file in self:
            files.append({"filename": basename(file.name), "size": int(file.size)})
        return json.dumps(files, indent=indent)


class SeaDexTorrent:
    def __init__(self, file: StrPath) -> None:
        """
        Class to handle torrent files for SeaDex.

        Parameters
        ----------
        file : StrPath
            The path to the torrent file.

        """
        self._file = realpath(file)

    @property
    def file(self) -> Path:
        """Resolved path to the torrent file."""
        return self._file

    @cached_property
    def filelist(self) -> FileList:
        """List of files within the torrent."""
        torrent = TorfTorrent.read(self.file)
        files = []
        for file in torrent.files:
            files.append(File(name=file, size=file.size))
        return FileList(files)

    def sanitize(self, *, destination: StrPath | None = None, overwrite: bool = False) -> Path:
        """
        Sanitizes the torrent file by removing sensitive data and optionally saves it to a new location.

        Parameters
        ----------
        destination : StrPath | None, optional
            The destination path to save the sanitized torrent. If None, the sanitized file is saved in place.
        overwrite : bool, optional
            If True, overwrites the existing file or destination file if it exists.

        Returns
        -------
        Path
            The path to the sanitized torrent file.

        Raises
        ------
        FileExistsError
            - If `destination` is None and `overwrite` is False.
            - If `destination` already exists and `overwrite` is False.

        Notes
        -----
        - If the torrent file is public (i.e., not marked as private), it is returned as is.
        - The following fields are removed from the torrent file if it is private:
            - Trackers
            - Web seeds
            - HTTP seeds
            - Private flag
            - Comment
            - Creation date
            - Created by field
            - Source field
        - The torrent's `infohash` is randomized.

        """
        torrent = TorfTorrent.read(self.file)

        if not torrent.private:
            # Public torrent
            return self.file

        torrent.trackers = None
        torrent.webseeds = None
        torrent.httpseeds = None
        torrent.private = None
        torrent.comment = None
        torrent.creation_date = None
        torrent.created_by = None
        torrent.source = None
        torrent.randomize_infohash = True

        if destination is None:
            if overwrite is False:
                raise FileExistsError(self.file)
            torrent.write(self.file, overwrite=True)
            return self.file
        destination = realpath(destination)
        torrent.write(destination, overwrite=overwrite)
        return destination
