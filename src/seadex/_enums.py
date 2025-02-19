from __future__ import annotations

import base64

from stringenum import CaseInsensitiveStrEnum


class Tracker(CaseInsensitiveStrEnum):
    """Enum of public and private trackers."""

    # Public Trackers
    NYAA = "Nyaa"
    ANIMETOSHO = "AnimeTosho"
    ANIDEX = "AniDex"
    RUTRACKER = "RuTracker"
    # Private Trackers
    ANIMEBYTES = "AB"
    BEYONDHD = "BeyondHD"
    PASSTHEPOPCORN = "PassThePopcorn"
    BROADCASTTHENET = "BroadcastTheNet"
    HDBITS = "HDBits"
    BLUTOPIA = "Blutopia"
    AITHER = "Aither"
    OTHER = "Other"
    OTHER_PRIVATE = "OtherPrivate"

    def is_public(self) -> bool:
        """
        Check if the current tracker is public.

        Returns
        -------
        bool
            `True` if the tracker is public, `False` otherwise.

        """
        return self.value in ("Nyaa", "AnimeTosho", "AniDex", "RuTracker", "Other")

    def is_private(self) -> bool:
        """
        Check if the current tracker is private.

        Returns
        -------
        bool
            `True` if the tracker is private, `False` otherwise.

        """
        return not self.is_public()

    @property
    def url(self) -> str:
        """
        URL of the current tracker.

        Returns
        -------
        str
            URL of the tracker.

        Notes
        -----
        Returns an empty string for [`Tracker.OTHER`][seadex.Tracker.OTHER] and [`Tracker.OTHER_PRIVATE`][seadex.Tracker.OTHER_PRIVATE].

        """
        _map = {
            "NYAA": b"aHR0cHM6Ly9ueWFhLnNp",
            "ANIMETOSHO": b"aHR0cHM6Ly9hbmltZXRvc2hvLm9yZw==",
            "ANIDEX": b"aHR0cHM6Ly9hbmlkZXguaW5mbw==",
            "RUTRACKER": b"aHR0cHM6Ly9ydXRyYWNrZXIub3Jn",
            "ANIMEBYTES": b"aHR0cHM6Ly9hbmltZWJ5dGVzLnR2",
            "BEYONDHD": b"aHR0cHM6Ly9iZXlvbmQtaGQubWU=",
            "PASSTHEPOPCORN": b"aHR0cHM6Ly9wYXNzdGhlcG9wY29ybi5tZQ==",
            "BROADCASTTHENET": b"aHR0cHM6Ly9icm9hZGNhc3RoZS5uZXQ=",
            "HDBITS": b"aHR0cHM6Ly9oZGJpdHMub3Jn",
            "BLUTOPIA": b"aHR0cHM6Ly9ibHV0b3BpYS5jYw==",
            "AITHER": b"aHR0cHM6Ly9haXRoZXIuY2M=",
            "OTHER": b"",
            "OTHER_PRIVATE": b"",
        }

        return base64.b64decode(_map[self.name]).decode()
