from __future__ import annotations

from pathlib import Path

from torf import Torrent

from seadex._types import StrPath


def sanitize_torrent(file: StrPath, *, destination: StrPath | None = None, overwrite: bool = False) -> Path:
    """
    Sanitizes a torrent file by removing sensitive data and optionally saves it to a new location.

    Parameters
    ----------
    file : StrPath
        The path to the torrent file to sanitize.
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
    file = Path(file).expanduser().resolve()
    torrent = Torrent.read(file)

    if not torrent.private:
        # Public torrent
        return file

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
            raise FileExistsError(f"{file} already exists!")
        else:
            torrent.write(file, overwrite=True)
            return file
    else:
        destination = Path(destination).expanduser().resolve()
        torrent.write(destination, overwrite=overwrite)
        return destination
