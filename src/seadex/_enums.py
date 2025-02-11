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
    PRIVATE_TRACKER = "PT"
    BEYONDHD = "BeyondHD"
    PASSTHEPOPCORN = "PassThePopcorn"
    BROADCASTTHENET = "BroadcastTheNet"
    HDBITS = "HDBits"
    BLUTOPIA = "Blutopia"
    AITHER = "Aither"
    OTHER = "Other"

    def is_private(self) -> bool:
        """
        Check if the current tracker is private.

        Returns
        -------
        bool
            `True` if the tracker is private, `False` otherwise.

        """
        return False if self.value in ("Nyaa", "AnimeTosho", "AniDex", "RuTracker") else True

    def is_public(self) -> bool:
        """
        Check if the current tracker is public.

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
        _map = {
            # Public Trackers
            "NYAA": b"bnlhYS5zaQ==",
            "ANIMETOSHO": b"YW5pbWV0b3Noby5vcmc=",
            "ANIDEX": b"YW5pZGV4LmluZm8=",
            "RUTRACKER": b"cnV0cmFja2VyLm9yZw==",
            # Private Trackers
            "PRIVATE_TRACKER": b"YW5pbWVieXRlcy50dg==",
            "BEYONDHD": b"YmV5b25kLWhkLm1l",
            "PASSTHEPOPCORN": b"cGFzc3RoZXBvcGNvcm4ubWU=",
            "BROADCASTTHENET": b"YnJvYWRjYXN0aGUubmV0",
            "HDBITS": b"aGRiaXRzLm9yZw==",
            "BLUTOPIA": b"Ymx1dG9waWEuY2M=",
            "AITHER": b"YWl0aGVyLmNj",
            "OTHER": b"",
        }

        return base64.b64decode(_map[self.name]).decode()
