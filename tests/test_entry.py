from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from seadex import SeaDexEntry


def test_properties(seadex_entry: SeaDexEntry) -> None:
    assert seadex_entry.base_url == "https://releases.moe"


def test_from_anilist_id(seadex_entry: SeaDexEntry) -> None:
    assert seadex_entry.from_id(165790).anilist_id == 165790


def test_from_seadex_id(seadex_entry: SeaDexEntry) -> None:
    assert seadex_entry.from_id("c344w8ld7q1yppz").anilist_id == 165790


def test_from_title(seadex_entry: SeaDexEntry) -> None:
    assert seadex_entry.from_title("tamako love story").anilist_id == 165790


def test_from_filename(seadex_entry: SeaDexEntry) -> None:
    entries = seadex_entry.from_filename("[SubsPlease] Kekkon suru tte, Hontou desu ka - 01 (1080p) [29AE676E].mkv")
    entry = next(entries)
    assert entry.anilist_id == 165790


def test_from_infohash(seadex_entry: SeaDexEntry) -> None:
    entries = tuple(seadex_entry.from_infohash("c4c1031570089d70bff40e1a89253025ad1cead7"))
    assert len(entries) == 1
    entry = entries[0]
    assert entry.anilist_id == 165790


def test_from_filter(seadex_entry: SeaDexEntry) -> None:
    assert next(seadex_entry.from_filter(f"alID={165790}")) == seadex_entry.from_id(165790)


def test_iterator(seadex_entry: SeaDexEntry) -> None:
    assert next(seadex_entry.iterator()) == seadex_entry.from_id(165790)
