from __future__ import annotations

import base64

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
        (Tracker.OTHER_PRIVATE, "OtherPrivate"),
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
        ("OtherPrivate", True, False),
    ],
)
def test_tracker_is_private(tracker: str, is_private: bool, is_public: bool) -> None:
    assert Tracker(tracker).is_private() == is_private
    assert Tracker(tracker).is_public() == is_public


@pytest.mark.parametrize(
    "tracker, url",
    [
        ("Nyaa", b"aHR0cHM6Ly9ueWFhLnNp"),
        ("AnimeTosho", b"aHR0cHM6Ly9hbmltZXRvc2hvLm9yZw=="),
        ("AniDex", b"aHR0cHM6Ly9hbmlkZXguaW5mbw=="),
        ("RuTracker", b"aHR0cHM6Ly9ydXRyYWNrZXIub3Jn"),
        ("AB", b"aHR0cHM6Ly9hbmltZWJ5dGVzLnR2"),
        ("BeyondHD", b"aHR0cHM6Ly9iZXlvbmQtaGQubWU="),
        ("PassThePopcorn", b"aHR0cHM6Ly9wYXNzdGhlcG9wY29ybi5tZQ=="),
        ("BroadcastTheNet", b"aHR0cHM6Ly9icm9hZGNhc3RoZS5uZXQ="),
        ("HDBits", b"aHR0cHM6Ly9oZGJpdHMub3Jn"),
        ("Blutopia", b"aHR0cHM6Ly9ibHV0b3BpYS5jYw=="),
        ("Aither", b"aHR0cHM6Ly9haXRoZXIuY2M="),
        ("Other", b""),
        ("OtherPrivate", b""),
    ],
)
def test_tracker_domain(tracker: str, url: bytes) -> None:
    assert Tracker(tracker).url == base64.b64decode(url).decode()


def test_bad_value() -> None:
    with pytest.raises(ValueError):
        Tracker("kasdjsahdjshdahdakjds")

    with pytest.raises(ValueError):
        Tracker(121212)  # type: ignore[arg-type]


def test_case_insensitive_lookup() -> None:
    assert Tracker("nyAA") is Tracker.NYAA
    assert Tracker("ANIMETOSHO") is Tracker.ANIMETOSHO
    assert Tracker("Ab") is Tracker.ANIMEBYTES
