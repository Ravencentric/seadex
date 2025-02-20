from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from zipfile import ZipFile

import pytest
from pydantic import ByteSize
from pytest_httpx import HTTPXMock

from seadex import BackupFile, BadBackupFileError, SeaDexBackup


def test_backupfile() -> None:
    backupfile = BackupFile(
        name="test.zip",
        size=ByteSize(1024),
        modified_time=datetime(2024, 9, 12, 18, 14, 33, 816632, tzinfo=timezone.utc),
    )

    assert str(backupfile) == backupfile.name
    assert backupfile.size == ByteSize(1024)
    assert backupfile.modified_time == datetime(2024, 9, 12, 18, 14, 33, 816632, tzinfo=timezone.utc)


def test_backup_properties(seadex_backup: SeaDexBackup, httpx_mock: HTTPXMock) -> None:
    sample = [
        {"key": "@auto_pb_backup_sea_dex_20241116000000.zip", "size": 65571703, "modified": "2024-11-16 00:00:04.982Z"},
        {"key": "@auto_pb_backup_sea_dex_20241117000000.zip", "size": 65526931, "modified": "2024-11-17 00:00:03.423Z"},
        {"key": "@auto_pb_backup_sea_dex_20241118000000.zip", "size": 65899588, "modified": "2024-11-18 00:00:03.390Z"},
        {"key": "@auto_pb_backup_sea_dex_20241119000000.zip", "size": 66651413, "modified": "2024-11-19 00:00:03.511Z"},
        {"key": "@auto_pb_backup_sea_dex_20241120000000.zip", "size": 66249632, "modified": "2024-11-20 00:00:03.784Z"},
        {"key": "@auto_pb_backup_sea_dex_20241121000000.zip", "size": 65304056, "modified": "2024-11-21 00:00:03.661Z"},
        {"key": "@auto_pb_backup_sea_dex_20241122000000.zip", "size": 65847001, "modified": "2024-11-22 00:00:03.487Z"},
    ]
    httpx_mock.add_response(url="https://releases.moe/api/backups", json=sample, is_reusable=True)
    assert seadex_backup.base_url == "https://releases.moe"
    assert len(seadex_backup.backups) == 7
    assert seadex_backup.latest_backup == BackupFile(
        name="@auto_pb_backup_sea_dex_20241122000000.zip",
        size=65847001,  # type: ignore[arg-type]
        modified_time=datetime(2024, 11, 22, 0, 0, 3, 487000, tzinfo=timezone.utc),
    )


def test_backup_download_with_invalid_destination(seadex_backup: SeaDexBackup, tmp_path: Path) -> None:
    with pytest.raises(NotADirectoryError):
        seadex_backup.download(destination=tmp_path / "doesnt exist")


def test_backup_download(
    seadex_backup: SeaDexBackup, httpx_mock: HTTPXMock, tmp_path_factory: pytest.TempPathFactory
) -> None:
    sample = [
        {"key": "@auto_pb_backup_sea_dex_20241120000000.zip", "size": 66249632, "modified": "2024-11-20 00:00:03.784Z"},
        {"key": "@auto_pb_backup_sea_dex_20241121000000.zip", "size": 65304056, "modified": "2024-11-21 00:00:03.661Z"},
        {"key": "@auto_pb_backup_sea_dex_20241122000000.zip", "size": 65847001, "modified": "2024-11-22 00:00:03.487Z"},
    ]
    httpx_mock.add_response(url="https://releases.moe/api/backups", json=sample, is_reusable=True)

    latest_backup = seadex_backup.latest_backup
    sample_backup_file = tmp_path_factory.mktemp("blah") / "sample_backup.zip"

    with ZipFile(sample_backup_file, "w") as f:
        f.writestr("data.db", data=b"hello world")

    httpx_mock.add_response(
        url=f"https://releases.moe/api/backups/{latest_backup.name}?token=secret",
        content=sample_backup_file.read_bytes(),
        is_reusable=True,
    )

    zip_with_bad_crc = f"{uuid4()}.zip"

    httpx_mock.add_response(
        url=f"https://releases.moe/api/backups/{zip_with_bad_crc}?token=secret",
        # https://github.com/python/cpython/blob/f1e74248025b36a0c5d12f72c4ab713f4682f523/Lib/test/test_zipfile/test_core.py#L2435-L2443
        content=(
            b"PK\003\004\024\0\0\0\0\0 \213\212;:r"
            b"\253\377\f\0\0\0\f\0\0\0\005\0\0\000af"
            b"ilehello,AworldP"
            b"K\001\002\024\003\024\0\0\0\0\0 \213\212;:"
            b"r\253\377\f\0\0\0\f\0\0\0\005\0\0\0\0"
            b"\0\0\0\0\0\0\0\200\001\0\0\0\000afi"
            b"lePK\005\006\0\0\0\0\001\0\001\0003\000"
            b"\0\0/\0\0\0\0\0"
        ),
    )

    backup1 = seadex_backup.download(destination=tmp_path_factory.mktemp("blah2"))
    backup2 = seadex_backup.download(latest_backup, destination=tmp_path_factory.mktemp("blah3"))
    backup3 = seadex_backup.download(
        "@auto_pb_backup_sea_dex_20241122000000.zip", destination=tmp_path_factory.mktemp("blah3")
    )

    assert backup1.name == latest_backup.name
    assert backup2.name == latest_backup.name
    assert backup3.name == latest_backup.name

    with pytest.raises(TypeError):
        seadex_backup.download(1213123, destination=tmp_path_factory.mktemp("blah4"))  # type: ignore[arg-type]

    with pytest.raises(BadBackupFileError):
        seadex_backup.download(zip_with_bad_crc, destination=tmp_path_factory.mktemp("blah5"))


def test_backup_create(seadex_backup: SeaDexBackup) -> None:
    with pytest.raises(ValueError):
        seadex_backup.create("@invalid_character.zip")


def test_backup_create_with_invalid_filename(seadex_backup: SeaDexBackup, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://releases.moe/api/backups",
        method="POST",
        json={"name": "seadex-backup.zip"},
        headers={"Authorization": "secret"},
    )
    sample = [
        {"key": "@auto_pb_backup_sea_dex_20241120000000.zip", "size": 66249632, "modified": "2024-11-20 00:00:03.784Z"},
        {"key": "@auto_pb_backup_sea_dex_20241121000000.zip", "size": 65304056, "modified": "2024-11-21 00:00:03.661Z"},
        {"key": "seadex-backup.zip", "size": 65847001, "modified": "2024-11-23 00:00:03.487Z"},
    ]
    httpx_mock.add_response(url="https://releases.moe/api/backups", method="GET", json=sample)

    backup = seadex_backup.create("seadex-backup.zip")
    assert backup.name == "seadex-backup.zip"


def test_backup_delete(seadex_backup: SeaDexBackup, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(url="https://releases.moe/api/backups/seadex-backup.zip", method="DELETE")
    seadex_backup.delete("seadex-backup.zip")
