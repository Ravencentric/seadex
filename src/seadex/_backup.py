from __future__ import annotations

import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin
from uuid import uuid4
from zipfile import BadZipFile, ZipFile

from httpx import Client
from pydantic import ByteSize
from typing_extensions import assert_never

from seadex._models import FrozenBaseModel
from seadex._types import StrPath, UTCDateTime
from seadex._utils import realpath

if TYPE_CHECKING:
    from typing_extensions import Self


class BackupFile(FrozenBaseModel):
    """A model representing a backup file."""

    name: str
    """The name of the backup file."""
    size: ByteSize
    """The size of the backup file in bytes."""
    modified_time: UTCDateTime
    """The last modified time of the backup file."""

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

    @classmethod
    def _from_dict(cls, dictionary: dict[str, Any], /) -> Self:
        """Parses the response from the SeaDex Backup API into a `BackupFile` object."""
        kwargs = {
            "name": dictionary["key"],
            "modified_time": dictionary["modified"],
            "size": dictionary["size"],
        }
        return cls.model_validate(kwargs)


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

        Examples
        --------
        ```py
        with SeaDexBackup("me@email.com", "password") as seadex_backup:
            print(seadex_backup.latest_backup)
            #> @auto_pb_backup_sea_dex_20241122000000.zip
        ```

        Notes
        -----
        Only SeaDex admins can use this! Logging in with a non-admin account will result in failure.
        """
        self._url = url
        self._client = Client()
        self._admin_token = self._auth_with_password(email, password)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        """
        Closes the underlying HTTP client connection.
        """
        self._client.close()

    def _url_for(self, endpoint: str) -> str:
        return urljoin(self._url, endpoint)

    def _auth_with_password(self, email: str, password: str) -> str:
        response = self._client.post(
            self._url_for("/api/admins/auth-with-password"), json={"identity": email, "password": password}
        )
        admin = response.raise_for_status().json()
        return admin["token"]  # type: ignore[no-any-return]

    def _get_file_token(self) -> str:
        response = self._client.post(self._url_for("/api/files/token"), headers={"Authorization": self._admin_token})
        return response.raise_for_status().json()["token"]  # type: ignore[no-any-return]

    @property
    def backups(self) -> tuple[BackupFile, ...]:
        """
        Retrieves a sorted tuple of all backup files.

        Returns
        -------
        tuple[BackupFile, ...]
            A tuple of all backup files, sorted by the modified date.
        """

        response = self._client.get(
            "https://releases.moe/api/backups", headers={"Authorization": self._admin_token}
        ).json()
        backups = (BackupFile._from_dict(backup) for backup in response)
        return tuple(sorted(backups, key=lambda f: f.modified_time))

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

    def download(self, file: str | BackupFile | None = None, *, destination: StrPath = Path.cwd()) -> Path:
        """
        Downloads a specified backup file to the given destination directory.

        Parameters
        ----------
        file : str | BackupFile | None, optional
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
            case str():
                key = file
            case BackupFile():
                key = file.name
            case _:
                assert_never(file)

        outfile = destination / key

        with TemporaryDirectory(ignore_cleanup_errors=True) as tmpdir:
            tmpfile = Path(tmpdir).resolve() / str(uuid4())
            response = self._client.get(self._url_for(f"/api/backups/{key}"), params={"token": self._get_file_token()})
            tmpfile.write_bytes(response.content)
            shutil.move(tmpfile, outfile)

        with ZipFile(outfile) as archive:
            check = archive.testzip()

        if check is not None:
            outfile.unlink(missing_ok=True)
            raise BadZipFile(f"{outfile} failed integrity check!")

        return outfile

    def create(self, filename: str) -> BackupFile:
        """
        Create a new backup with the specified filename.

        Parameters
        ----------
        filename : str
            The name to assign to the backup file.
            This can include full formatting options as supported by
            [`datetime.strftime`][datetime.datetime.strftime].

        Returns
        -------
        BackupFile
            The newly created backup file.
        """
        _filename = filename.removesuffix(".zip") + ".zip"
        _filename = datetime.now(timezone.utc).strftime(_filename).casefold()

        if re.match(r"^([a-z0-9_-]+\.zip)$", _filename) is None:
            # The API forbids anything else, so we need to enforce it.
            raise ValueError(
                f"Invalid filename: {_filename!r}. The filename may only contain alphanumeric characters, hyphens, or underscores."
            )

        self._client.post(
            self._url_for("/api/backups"), json={"name": _filename}, headers={"Authorization": self._admin_token}
        ).raise_for_status()

        return next(filter(lambda member: member.name == _filename, self.backups))

    def delete(self, file: str | BackupFile) -> None:
        """
        Delete the specified backup file.

        Parameters
        ----------
        file : str | BackupFile
            The backup file to delete.

        Returns
        -------
        None
        """
        self._client.delete(
            self._url_for(f"/api/backups/{file}"), headers={"Authorization": self._admin_token}
        ).raise_for_status()
