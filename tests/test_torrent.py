from __future__ import annotations

from pathlib import Path

from torf import Torrent

from seadex import sanitize_torrent


def test_sanitize_private_torrent(tmp_path: Path) -> None:
    file = "tests/__torrents__/private-ubuntu-24.04.1-desktop-amd64.iso.torrent"
    original = Torrent.read(file)
    sanitized = Torrent.read(
        sanitize_torrent(
            file, destination=tmp_path / "private-ubuntu-24.04.1-desktop-amd64.iso.torrent", overwrite=True
        )
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


def test_sanitize_public_torrent(tmp_path: Path) -> None:
    file = "tests/__torrents__/public-ubuntu-24.04.1-desktop-amd64.iso.torrent"
    original = Torrent.read(file)
    sanitized = Torrent.read(
        sanitize_torrent(file, destination=tmp_path / "public-ubuntu-24.04.1-desktop-amd64.iso.torrent", overwrite=True)
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
