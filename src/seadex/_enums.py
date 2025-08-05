from __future__ import annotations

import base64
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Self

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


class CaseInsensitiveStrEnum(StrEnum):
    """StrEnum with case-insensitive lookup."""

    @classmethod
    def _missing_(cls, value: object) -> Self:
        # https://docs.python.org/3/library/enum.html#enum.Enum._missing_
        msg = f"'{value}' is not a valid {cls.__name__}"

        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
            raise ValueError(msg)
        raise ValueError(msg)


class Tag(CaseInsensitiveStrEnum):
    """Torrent tags."""

    DOLBY_VISION = "Dolby Vision"
    """This release is Dolby Vision Profile 5 which will not display correctly on unsupported setups."""

    HDR = "HDR"
    """This release is HDR which will not display correctly on unsupported setups."""

    DEBAND_REQUIRED = "Deband Required"
    """
    This release requires the use of MPV Deband (Press b).
    If you cannot deband, get the alt release.
    """

    DEBAND_RECOMMENDED = "Deband Recommended"
    """
    This release recommends the use of MPV Deband (Press b).
    If you cannot deband, still get this release.
    """

    YUV444P = "YUV444P"
    """
    This release is encoded in YUV444P which has poor hardware support,
    make sure your device can play it properly or get the alt release.
    """

    PATCH_REQUIRED = "Patch Required"
    """This release requires you to download an external patch to fix issues."""

    MISPLACED_SPECIAL = "Misplaced Special"
    """
    This release has specials at the top of the file list,
    make sure you watch the episodes in the correct order.
    """

    VFR = "VFR"
    """
    This release has a variable framerate, your screen should
    be set to a multiple of 120hz or use VRR to display it correctly.
    """

    INCOMPLETE = "Incomplete"
    """This release does not contain all the episodes."""

    BROKEN = "Broken"
    """This release has issues, see notes for more information."""


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
        Returns an empty string for [`Tracker.OTHER`][seadex.Tracker.OTHER]
        and [`Tracker.OTHER_PRIVATE`][seadex.Tracker.OTHER_PRIVATE].

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
