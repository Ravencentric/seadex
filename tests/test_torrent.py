from __future__ import annotations

import json
import shutil
from os import fspath
from pathlib import Path

import pytest
from torf import Torrent

from seadex import SeaDexTorrent


def test_sanitize_file_exists_error() -> None:
    file = "tests/__torrents__/private-ubuntu-24.04.1-desktop-amd64.iso.torrent"
    with pytest.raises(FileExistsError):
        SeaDexTorrent(file).sanitize()


def test_sanitize_private_torrent(tmp_path: Path) -> None:
    file = "tests/__torrents__/private-ubuntu-24.04.1-desktop-amd64.iso.torrent"
    original = Torrent.read(file)
    sanitized = Torrent.read(
        SeaDexTorrent(file).sanitize(destination=tmp_path / "private-ubuntu-24.04.1-desktop-amd64.iso.torrent")
    )

    assert original.trackers is not None
    assert sanitized.trackers == []

    assert original.webseeds is not None
    assert sanitized.webseeds == []

    assert original.httpseeds is not None
    assert sanitized.httpseeds == []

    assert original.private is True
    assert sanitized.private is None

    assert original.comment is not None
    assert sanitized.comment is None

    assert original.creation_date is not None
    assert sanitized.creation_date is None

    assert original.created_by is not None
    assert sanitized.created_by is None

    assert original.source is not None
    assert sanitized.source is None

    assert original.infohash != sanitized.infohash
    assert original.infohash_base32 != sanitized.infohash_base32


def test_sanitize_private_torrent_with_overwrite(tmp_path: Path) -> None:
    src = "tests/__torrents__/private-ubuntu-24.04.1-desktop-amd64.iso.torrent"
    testfile = Path(shutil.copy(src, tmp_path))

    assert testfile.is_file()

    original = Torrent.read(testfile)
    sanitized = Torrent.read(SeaDexTorrent(testfile).sanitize(overwrite=True))

    assert original.trackers is not None
    assert sanitized.trackers == []

    assert original.webseeds is not None
    assert sanitized.webseeds == []

    assert original.httpseeds is not None
    assert sanitized.httpseeds == []

    assert original.private is True
    assert sanitized.private is None

    assert original.comment is not None
    assert sanitized.comment is None

    assert original.creation_date is not None
    assert sanitized.creation_date is None

    assert original.created_by is not None
    assert sanitized.created_by is None

    assert original.source is not None
    assert sanitized.source is None

    assert original.infohash != sanitized.infohash
    assert original.infohash_base32 != sanitized.infohash_base32


def test_sanitize_public_torrent(tmp_path: Path) -> None:
    file = "tests/__torrents__/public-ubuntu-24.04.1-desktop-amd64.iso.torrent"
    original = Torrent.read(file)
    sanitized = Torrent.read(
        SeaDexTorrent(file).sanitize(
            destination=tmp_path / "public-ubuntu-24.04.1-desktop-amd64.iso.torrent", overwrite=True
        )
    )

    assert original.trackers == sanitized.trackers
    assert original.webseeds == sanitized.webseeds
    assert original.httpseeds == sanitized.httpseeds
    assert original.private == sanitized.private
    assert original.comment == sanitized.comment
    assert original.creation_date == sanitized.creation_date
    assert original.created_by == sanitized.created_by
    assert original.source == sanitized.source
    assert original.infohash == sanitized.infohash
    assert original.infohash_base32 == sanitized.infohash_base32


def test_filelist_public() -> None:
    file = "tests/__torrents__/public-ubuntu-24.04.1-desktop-amd64.iso.torrent"

    original = Torrent.read(file)
    seadex = SeaDexTorrent(file)

    original_files = [{"filename": Path(file).as_posix(), "size": int(file.size)} for file in original.files]
    seadex_filelist = [{"filename": file.name, "size": file.size} for file in seadex.filelist]
    seadex_filelist_str = [{"filename": str(file), "size": file.size} for file in seadex.filelist]
    seadex_filelist_fspath = [{"filename": fspath(file), "size": file.size} for file in seadex.filelist]

    assert original_files == seadex_filelist == seadex_filelist_str == seadex_filelist_fspath


def test_filelist_private() -> None:
    file = "tests/__torrents__/private-ubuntu-24.04.1-desktop-amd64.iso.torrent"

    original = Torrent.read(file)
    seadex = SeaDexTorrent(file)

    original_files = [{"filename": Path(file).as_posix(), "size": int(file.size)} for file in original.files]
    seadex_filelist = [{"filename": file.name, "size": file.size} for file in seadex.filelist]
    seadex_filelist_str = [{"filename": str(file), "size": file.size} for file in seadex.filelist]
    seadex_filelist_fspath = [{"filename": fspath(file), "size": file.size} for file in seadex.filelist]

    assert original_files == seadex_filelist == seadex_filelist_str == seadex_filelist_fspath


def test_filelist_json_private() -> None:
    file = "tests/__torrents__/private-ubuntu-24.04.1-desktop-amd64.iso.torrent"

    original = Torrent.read(file)
    seadex = SeaDexTorrent(file)

    original_files = json.dumps([{"filename": Path(file).name, "size": int(file.size)} for file in original.files])

    assert original_files == seadex.filelist.to_json()


def test_filelist_json_public() -> None:
    file = "tests/__torrents__/public-ubuntu-24.04.1-desktop-amd64.iso.torrent"

    original = Torrent.read(file)
    seadex = SeaDexTorrent(file)

    original_files = json.dumps([{"filename": Path(file).name, "size": int(file.size)} for file in original.files])

    assert original_files == seadex.filelist.to_json()
