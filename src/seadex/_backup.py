from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin
from zipfile import ZipFile

import httpx
import msgspec
from atomicwriter import AtomicWriter
from httpx import Client

from seadex._exceptions import BadBackupFileError
from seadex._types import Base, StrPath
from seadex._utils import httpx_client, realpath

if TYPE_CHECKING:
    from typing_extensions import Self


class BackupFile(Base, frozen=True, kw_only=True):
    """Represents a backup file."""

    name: str
    """The name of the backup file."""
    size: int
    """The size of the backup file in bytes."""
    modified_time: datetime
    """The last modified time of the backup file."""

    def __str__(self) -> str:
        """Implement the string representation. Equivalent to `BackupFile.name`."""
        return self.name

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
        try:
            # Attempt a strict conversion, assuming data
            # comes from TorrentRecord.to_dict()
            return msgspec.convert(data, type=cls)
        except msgspec.ValidationError:
            # Failed, let's attempt a laxer conversion,
            # assuming the data comes from the SeaDex API.
            kwargs = {
                "name": data["key"],
                "modified_time": data["modified"],
                "size": data["size"],
            }
            return msgspec.convert(kwargs, type=cls, strict=False)


class SeaDexBackup:
    def __init__(
        self,
        email: str,
        password: str,
        *,
        base_url: str = "https://releases.moe",
        client: Client | None = None,
    ) -> None:
        """
        Client to interact with the SeaDex backup API.

        Parameters
        ----------
        email : str
            The email address for authentication.
        password : str
            The password for authentication.
        base_url : str, optional
            The base URL of SeaDex, used for constructing API queries.
        client : Client, optional
            An [`httpx.Client`][httpx.Client] instance used to make requests to SeaDex.

            [httpx.Client]: https://www.python-httpx.org/advanced/#client

        Examples
        --------
        ```py
        with SeaDexBackup("me@email.com", "password") as seadex_backup:
            print(seadex_backup.get_latest_backup())
            #> @auto_pb_backup_sea_dex_20241122000000.zip
        ```

        Notes
        -----
        Only SeaDex admins can use this! Logging in with a non-admin account will result in failure.

        """
        self._base_url = base_url
        # Increase client timeout to 60s for backup operations.
        # Their large and growing size (>= 160 MB) can cause
        # methods like create() to exceed the default 5s timeout.
        self._client = httpx_client(timeout=httpx.Timeout(60)) if client is None else client
        self._admin_token = self._auth_with_password(email, password)

    @property
    def base_url(self) -> str:
        """
        Base URL, used for constructing API queries.
        """
        return self._base_url

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        """
        Close the underlying HTTP client connection.
        """
        self._client.close()

    def _url_for(self, endpoint: str) -> str:
        return urljoin(self._base_url, endpoint)

    def _auth_with_password(self, email: str, password: str) -> str:
        response = self._client.post(
            self._url_for("/api/admins/auth-with-password"), json={"identity": email, "password": password}
        )
        admin = response.raise_for_status().json()
        return admin["token"]  # type: ignore[no-any-return]

    def _get_file_token(self) -> str:
        response = self._client.post(self._url_for("/api/files/token"), headers={"Authorization": self._admin_token})
        return response.raise_for_status().json()["token"]  # type: ignore[no-any-return]

    def get_backups(self) -> tuple[BackupFile, ...]:
        """
        Retrieve a tuple of backup files.

        Returns
        -------
        tuple[BackupFile, ...]
            A tuple of backup files, sorted by the modified date.

        """

        response = self._client.get(
            "https://releases.moe/api/backups", headers={"Authorization": self._admin_token}
        ).json()
        backups = [BackupFile.from_dict(backup) for backup in response]
        return tuple(sorted(backups, key=lambda f: f.modified_time))

    def get_latest_backup(self) -> BackupFile:
        """
        Retrieve the latest backup file.

        Returns
        -------
        BackupFile
            The latest backup file.

        """
        return self.get_backups()[-1]

    def download(
        self, file: str | BackupFile | None = None, *, destination: StrPath | None = None, overwrite: bool = False
    ) -> Path:
        """
        Download the specified backup file to the given destination directory.

        Parameters
        ----------
        file : str | BackupFile | None, optional
            The backup file to download.
            If `None`, downloads the [latest existing backup][seadex.SeaDexBackup.get_latest_backup].
        destination : StrPath | None, optional
            The destination directory to save the backup.
        overwrite : bool, optional
            Whether to overwrite the file if it already exists.

        Returns
        -------
        Path
            The path to the downloaded backup file.

        Raises
        ------
        NotADirectoryError
            If the destination is not a valid directory.
        BadBackupFileError
            If the downloaded backup file fails integrity check.
        TypeError
            If the provided `file` argument has an invalid type.

        """
        destination = Path.cwd() if destination is None else realpath(destination)

        if not destination.is_dir():
            errmsg = f"{destination} must be an existing directory!"
            raise NotADirectoryError(errmsg)

        match file:
            case None:
                key = self.get_latest_backup().name
            case str():
                key = file
            case BackupFile():
                key = file.name
            case _:
                errmsg = f"'file' must be a string or path-like, not {type(file).__name__}."
                raise TypeError(errmsg)

        outfile = destination / key

        with AtomicWriter(outfile, overwrite=overwrite) as f:
            url = self._url_for(f"/api/backups/{key}")
            params = {"token": self._get_file_token()}
            with self._client.stream("GET", url, params=params) as response:
                for chunk in response.iter_bytes(1024 * 1024):
                    f.write_bytes(chunk)

        with ZipFile(outfile) as archive:
            check = archive.testzip()

        if check is not None:
            outfile.unlink(missing_ok=True)
            errmsg = f"{outfile} failed integrity check!"
            raise BadBackupFileError(errmsg)

        return outfile

    def create(self, filename: str) -> BackupFile:
        """
        Create a new backup with the specified filename.

        Parameters
        ----------
        filename : str
            The name to assign to the backup file.
            The filename must contain only lowercase alphabets, numbers, hyphens, or underscores.
            It may also include formatting options as supported by [`datetime.strftime`][datetime.datetime.strftime].

        Returns
        -------
        BackupFile
            The newly created backup file.

        Raises
        ------
        ValueError
            If the filename is invalid.

        """
        _filename = filename.removesuffix(".zip") + ".zip"
        _filename = datetime.now(timezone.utc).strftime(_filename).casefold()

        if re.match(r"^([a-z0-9_-]+\.zip)$", _filename) is None:
            # The API forbids anything else, so we need to enforce it.
            errmsg = (
                f"Invalid filename: {_filename!r}. "
                "The filename may only contain lowercase alphabets, "
                "numbers, hyphens, or underscores."
            )
            raise ValueError(errmsg)

        self._client.post(
            self._url_for("/api/backups"),
            json={"name": _filename},
            headers={"Authorization": self._admin_token},
        ).raise_for_status()

        # https://boltons.readthedocs.io/en/latest/iterutils.html#boltons.iterutils.first
        return next(filter(lambda member: member.name == _filename, self.get_backups()))

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
