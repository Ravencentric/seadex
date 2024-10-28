from __future__ import annotations

from datetime import datetime, timezone
from os import PathLike
from os.path import basename
from pathlib import Path
from shutil import move
from tempfile import TemporaryDirectory
from uuid import uuid4
from zipfile import BadZipFile, ZipFile

from pocketbase import PocketBase
from pydantic import ByteSize
from typing_extensions import assert_never

from seadex._models import FrozenBaseModel
from seadex._types import StrPath, UTCDateTime
from seadex._utils import httpx_client, realpath


class BackupFile(FrozenBaseModel):
    """A model representing a backup file."""

    name: str
    """The name of the backup file."""
    size: ByteSize
    """The size of the backup file in bytes."""
    modified_time: UTCDateTime
    """The last modified time of the backup file."""

    def as_tuple(self) -> tuple[str, ByteSize, UTCDateTime]:
        """Returns the name, size, and modified time of the backup file as a tuple."""
        return (self.name, self.size, self.modified_time)

    def __str__(self) -> str:
        """String representation. Equivalent to `BackupFile.name`."""
        return self.name

    def __fspath__(self) -> str:
        """
        Path representation. Equivalent to `BackupFile.name`.
        Allows for compatibility with `PathLike` objects.

        Examples
        --------
        >>> from pathlib import Path
        >>> from seadex import BackupFile
        >>> backup = BackupFile(name="20240909041339-seadex-backup.zip", size=..., modified=..)
        >>> Path.home() / backup
        PosixPath('/home/raven/20240909041339-seadex-backup.zip')
        """
        return self.name


class SeaDexBackup:
    def __init__(self, email: str, password: str, url: str = "https://releases.moe") -> None:
        """
        A class to interact with the SeaDex backup API.

        Parameters
        ----------
        email : str
            The email address for authentication.
        password : str
            The password for authentication.
        url : str, optional
            The URL of SeaDex (default is "https://releases.moe").

        Notes
        -----
        Only SeaDex admins can use this! Logging in with a non-admin account will result in failure.
        """
        self.client = PocketBase(url, http_client=httpx_client())
        self.admin = self.client.admins.auth_with_password(email, password)

    @property
    def backups(self) -> tuple[BackupFile, ...]:
        """
        Retrieves a sorted tuple of all backup files.

        Returns
        -------
        tuple[BackupFile, ...]
            A tuple of all backup files, sorted by the modified date.
        """
        deduped = {
            BackupFile(name=file.key, size=file.size, modified_time=file.modified)  # type: ignore
            for file in self.client.backups.get_full_list()
        }

        return tuple(sorted(deduped, key=lambda f: f.modified_time))

    @property
    def latest_backup(self) -> BackupFile:
        """
        Retrieves the most recent backup file.

        Returns
        -------
        BackupFile
            The latest backup file.
        """
        return self.backups[-1]

    def download(self, file: StrPath | BackupFile | None = None, *, destination: StrPath = Path.cwd()) -> Path:
        """
        Downloads a specified backup file to the given destination directory.

        Parameters
        ----------
        file : StrPath | BackupFile | None, optional
            The backup file to download. If `None`, downloads the [latest existing backup][seadex.SeaDexBackup.latest_backup].
        destination : StrPath, optional
            The destination directory to save the backup.

        Returns
        -------
        Path
            The path to the downloaded backup file.

        Raises
        ------
        NotADirectoryError
            If the destination is not a valid directory.
        BadZipFile
            if the downloaded backup file fails integrity check.
        """
        destination = realpath(destination)

        if not destination.is_dir():
            raise NotADirectoryError(f"{destination} must be an existing directory!")

        match file:
            case None:
                key = self.latest_backup.name
            case str() | PathLike():
                key = basename(file)
            case _:  # pragma: no cover
                assert_never(file)

        outfile = destination / key

        with TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            tmpfile = Path(tmpdir).resolve() / str(uuid4())
            with tmpfile.open("wb") as fp:
                data = self.client.backups.download(key, self.client.get_file_token())  # type: ignore
                fp.write(data)
            try:
                tmpfile.replace(outfile)  # Attempt atomic replace
            except OSError:  # pragma: no cover
                # Failed, do a normal move
                move(tmpfile, outfile)

        with ZipFile(outfile) as archive:
            check = archive.testzip()
            if check is not None:  # pragma: no cover
                outfile.unlink(missing_ok=True)
                raise BadZipFile(f"{outfile} failed integrity check!")

        return outfile

    def create(self, filename: StrPath | None = None) -> BackupFile:  # pragma: no cover; TODO: Mock this in tests
        """
        Creates a new backup with an optional filename.

        Parameters
        ----------
        filename : StrPath | None, optional
            The name of the backup. If not provided, a default name is generated using the
            template `%Y%m%d%H%M%S-seadex-backup.zip`.
            This supports the full [`datetime.strftime`][datetime.datetime.strftime] formatting.

        Returns
        -------
        BackupFile
            The newly created backup file.
        """
        datefmt = "%Y%m%d%H%M%S"
        name = f"{datefmt}-seadex-backup.zip"

        if filename is None:  # pragma: no cover
            _filename = datetime.now(timezone.utc).strftime(name)
        else:
            _filename = basename(filename).removesuffix(".zip") + ".zip"
            _filename = datetime.now(timezone.utc).strftime(_filename)

        self.client.backups.create(_filename)

        return next(filter(lambda member: member.name == _filename, self.backups))

    def delete(self, file: StrPath | BackupFile) -> None:  # pragma: no cover; TODO: Mock this in tests
        """
        Deletes a specified backup file.

        Parameters
        ----------
        file : StrPath | BackupFile
            The backup file to delete.

        Returns
        -------
        None
        """
        self.client.backups.delete(basename(file))
