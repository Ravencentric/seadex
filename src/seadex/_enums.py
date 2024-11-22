from __future__ import annotations

from stringenum import CaseInsensitiveStrEnum


class Tracker(CaseInsensitiveStrEnum):
    """Enum of public and private trackers."""

    # Public Trackers
    NYAA = "Nyaa"
    ANIMETOSHO = "AnimeTosho"
    ANIDEX = "AniDex"
    RUTRACKER = "RuTracker"
    # Private Trackers
    ANIMEBYTES = "AnimeBytes"
    BEYONDHD = "BeyondHD"
    PASSTHEPOPCORN = "PassThePopcorn"
    BROADCASTTHENET = "BroadcastTheNet"
    HDBITS = "HDBits"
    BLUTOPIA = "Blutopia"
    AITHER = "Aither"
    OTHER = "Other"

    def is_private(self) -> bool:
        """
        Checks if the current tracker is private.

        Returns
        -------
        bool
            `True` if the tracker is private, `False` otherwise.
        """
        return False if self.value in ("Nyaa", "AnimeTosho", "AniDex", "RuTracker") else True

    def is_public(self) -> bool:
        """
        Checks if the current tracker is public.

        Returns
        -------
        bool
            `True` if the tracker is public, `False` otherwise.
        """
        return not self.is_private()

    @property
    def domain(self) -> str:
        """
        Returns the domain name associated with the current tracker.

        Returns
        -------
        str
            Domain name of the tracker, or an empty string for "Other".
        """
        return {
            # Public Trackers
            "NYAA": "nyaa.si",
            "ANIMETOSHO": "animetosho.org",
            "ANIDEX": "anidex.info",
            "RUTRACKER": "rutracker.org",
            # Private Trackers
            "ANIMEBYTES": "animebytes.tv",
            "BEYONDHD": "beyond-hd.me",
            "PASSTHEPOPCORN": "passthepopcorn.me",
            "BROADCASTTHENET": "broadcasthe.net",
            "HDBITS": "hdbits.org",
            "BLUTOPIA": "blutopia.cc",
            "AITHER": "aither.cc",
            "OTHER": "",
        }[self.name]
