from __future__ import annotations

from functools import cached_property
from pathlib import Path

from seadex._types import File, StrPath
from seadex._utils import realpath


class SeaDexTorrent:
    def __init__(self, file: StrPath) -> None:
        """
        Class to handle torrent files for SeaDex.

        Parameters
        ----------
        file : StrPath
            The path to the torrent file.

        """
        try:
            import torf
        except ModuleNotFoundError:  # pragma: no cover
            msg = (
                "The 'torf' library is required to use the SeaDexTorrent class.\n"
                "Please ensure you have installed SeaDex with the 'torrent' extra, "
                "typically specified as 'seadex[torrent]'."
            )
            raise ModuleNotFoundError(msg) from None

        self._file = realpath(file)
        self._torrent = torf.Torrent.read(self._file)

    @property
    def file(self) -> Path:
        """Resolved path to the torrent file."""
        return self._file

    @cached_property
    def filelist(self) -> tuple[File, ...]:
        """List of files within the torrent."""
        files = []
        for file in self._torrent.files:
            files.append(File(name=Path(file).as_posix(), size=file.size))
        return tuple(files)

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

        if not self._torrent.private:
            # Public torrent
            return self.file

        self._torrent.trackers = None
        self._torrent.webseeds = None
        self._torrent.httpseeds = None
        self._torrent.private = None
        self._torrent.comment = None
        self._torrent.creation_date = None
        self._torrent.created_by = None
        self._torrent.source = None
        self._torrent.randomize_infohash = True

        if destination is None:
            if overwrite is False:
                raise FileExistsError(self.file)
            self._torrent.write(self.file, overwrite=overwrite)
            return self.file
        destination = realpath(destination)
        self._torrent.write(destination, overwrite=overwrite)
        return destination
