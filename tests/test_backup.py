from __future__ import annotations

from datetime import datetime, timezone
from os import getenv
from pathlib import Path

import pytest
from pocketbase.utils import ClientResponseError
from pydantic import ByteSize

from seadex import BackupFile, SeaDexBackup

email = getenv("SEADEX_EMAIL")
password = getenv("SEADEX_PASSWORD")

cannot_authenticate = not (bool(email) and bool(password))

skip_if_cannot_authenticate = pytest.mark.skipif(
    cannot_authenticate,
    reason="Skipping test because backup endpoint requires authentication and no valid credentials are provided",
)


def test_bad_login() -> None:
    with pytest.raises(ClientResponseError):
        SeaDexBackup("aaaaaaaaaaaaa", "bbbbbbbbbbbbbbbb")


def test_backupfile() -> None:
    backupfile = BackupFile(
        name="test.zip",
        size=ByteSize(1024),
        modified_time=datetime(2024, 9, 12, 18, 14, 33, 816632, tzinfo=timezone.utc),
    )

    assert str(backupfile) == backupfile.name
    assert Path(backupfile) == Path(backupfile.name)
    assert backupfile.size == ByteSize(1024)
    assert backupfile.modified_time == datetime(2024, 9, 12, 18, 14, 33, 816632, tzinfo=timezone.utc)
    assert backupfile.as_tuple() == (
        "test.zip",
        1024,
        datetime(2024, 9, 12, 18, 14, 33, 816632, tzinfo=timezone.utc),
    )


@skip_if_cannot_authenticate
def test_backup_properties() -> None:
    client = SeaDexBackup(email, password)  # type: ignore
    assert len(client.backups) > 1
    assert client.latest_backup == client.backups[-1]


@skip_if_cannot_authenticate
def test_backup_download_with_invalid_destination(tmp_path: Path) -> None:
    client = SeaDexBackup(email, password)  # type: ignore

    with pytest.raises(NotADirectoryError):
        client.download(destination=tmp_path / "doesnt exist")


@skip_if_cannot_authenticate
def test_backup_download_without_filename(tmp_path: Path) -> None:
    client = SeaDexBackup(email, password)  # type: ignore
    latest_backup = client.latest_backup
    assert client.download(None, destination=tmp_path).name == latest_backup.name


@skip_if_cannot_authenticate
def test_backup_download_with_backupfile(tmp_path: Path) -> None:
    client = SeaDexBackup(email, password)  # type: ignore
    latest_backup = client.latest_backup
    assert client.download(latest_backup, destination=tmp_path).name == latest_backup.name


@skip_if_cannot_authenticate
def test_backup_download_with_pathlike(tmp_path: Path) -> None:
    client = SeaDexBackup(email, password)  # type: ignore
    latest_backup = client.latest_backup
    assert client.download(Path(latest_backup), destination=tmp_path).name == latest_backup.name


# TODO: Mock this test
# @skip_if_cannot_authenticate
# def test_backup_create() -> None:
#     client = SeaDexBackup(email, password)  # type: ignore
#     new_backup = client.create(Path(f"{uuid4()}-made-by-pytest.zip"))
#     assert new_backup in client.backups
#     client.delete(new_backup)
#     assert new_backup not in client.backups
