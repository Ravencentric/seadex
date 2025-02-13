from __future__ import annotations

import pytest

from seadex import Tracker


@pytest.mark.parametrize(
    "tracker, value",
    [
        (Tracker.NYAA, "Nyaa"),
        (Tracker.ANIMETOSHO, "AnimeTosho"),
        (Tracker.ANIDEX, "AniDex"),
        (Tracker.RUTRACKER, "RuTracker"),
        (Tracker.ANIMEBYTES, "AB"),
        (Tracker.BEYONDHD, "BeyondHD"),
        (Tracker.PASSTHEPOPCORN, "PassThePopcorn"),
        (Tracker.BROADCASTTHENET, "BroadcastTheNet"),
        (Tracker.HDBITS, "HDBits"),
        (Tracker.BLUTOPIA, "Blutopia"),
        (Tracker.AITHER, "Aither"),
        (Tracker.OTHER, "Other"),
    ],
)
def test_tracker_values(tracker: Tracker, value: str) -> None:
    assert tracker == value


@pytest.mark.parametrize(
    "tracker, is_private, is_public",
    [
        ("Nyaa", False, True),
        ("AnimeTosho", False, True),
        ("AniDex", False, True),
        ("RuTracker", False, True),
        ("AB", True, False),
        ("BeyondHD", True, False),
        ("PassThePopcorn", True, False),
        ("BroadcastTheNet", True, False),
        ("HDBits", True, False),
        ("Blutopia", True, False),
        ("Aither", True, False),
        ("Other", False, True),
    ],
)
def test_tracker_is_private(tracker: str, is_private: bool, is_public: bool) -> None:
    assert Tracker(tracker).is_private() == is_private
    assert Tracker(tracker).is_public() == is_public


@pytest.mark.parametrize(
    "tracker, domain",
    [
        ("Nyaa", "nyaa.si"),
        ("AnimeTosho", "animetosho.org"),
        ("AniDex", "anidex.info"),
        ("RuTracker", "rutracker.org"),
        ("BeyondHD", "beyond-hd.me"),
        ("PassThePopcorn", "passthepopcorn.me"),
        ("BroadcastTheNet", "broadcasthe.net"),
        ("HDBits", "hdbits.org"),
        ("Blutopia", "blutopia.cc"),
        ("Aither", "aither.cc"),
        ("Other", ""),
    ],
)
def test_tracker_domain(tracker: str, domain: str) -> None:
    assert Tracker(tracker).domain == domain


def test_bad_value() -> None:
    with pytest.raises(ValueError):
        Tracker("kasdjsahdjshdahdakjds")

    with pytest.raises(ValueError):
        Tracker(121212)


def test_case_insensitive_lookup() -> None:
    assert Tracker("nyAA") is Tracker.NYAA
    assert Tracker("ANIMETOSHO") is Tracker.ANIMETOSHO
    assert Tracker("Ab") is Tracker.ANIMEBYTES
