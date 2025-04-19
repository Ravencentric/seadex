from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin

import msgspec
from natsort import natsorted, ns

from seadex._enums import Tracker
from seadex._torrent import File
from seadex._types import Base

if TYPE_CHECKING:
    from typing_extensions import Self


class TorrentRecord(Base, frozen=True, kw_only=True):
    """Represents a single torrent record within a SeaDex entry."""

    collection_id: str
    """The ID of the collection the torrent record belongs to."""
    collection_name: str
    """The name of the collection the torrent record belongs to."""
    created_at: datetime
    """The timestamp of when the torrent record was created."""
    is_dual_audio: bool
    """Whether the torrent contains both Japanese and English audio tracks."""
    files: tuple[File, ...]
    """A tuple of `File` objects representing the files in the torrent."""
    id: str
    """The ID of the torrent record."""
    infohash: str | None
    """The infohash of the torrent if available, otherwise `None` (private torrents)."""
    is_best: bool
    """Whether this torrent is marked as the "best"."""
    release_group: str
    """The name of the group that released the torrent."""
    tracker: Tracker
    """The tracker where the torrent is hosted."""
    updated_at: datetime
    """The timestamp of when the torrent record was last updated."""
    url: str
    """The URL of the torrent."""
    size: int
    """The total size of the torrent, calculated by summing the sizes of all files."""

    @classmethod
    def from_dict(cls, data: dict[str, Any], /) -> Self:
        """
        Create an instance of this class from a dictionary.

        Parameters
        ----------
        data : dict[str, Any]
            Dictionary representing the instance of this class.

        Returns
        -------
        Self
            An instance of this class.

        """
        try:
            # Attempt a strict conversion, assuming data
            # comes from TorrentRecord.to_dict()
            return msgspec.convert(data, type=cls)
        except msgspec.ValidationError:
            # Failed, let's attempt a laxer conversion,
            # assuming the data comes from the SeaDex API.
            files = set()
            size = 0

            for file in data["files"]:
                files.add(File(name=file["name"], size=file["length"]))
                size += file["length"]

            # SeaDex API uses "<redacted>" to indicate that the torrent has no infohash (because it's private).
            # This replaces it with None for a more pythonic approach.
            infohash = None if data["infoHash"] == "<redacted>" else data["infoHash"]

            # Private trackers only have a relative URL on SeaDex
            # This will transform said relative URLs into absolute URLs.
            tracker = Tracker(data["tracker"])
            url: str = data["url"]
            if not url.startswith(tracker.url) and tracker.is_private():
                url = urljoin(tracker.url, url)

            kwargs = {
                "collection_id": data["collectionId"],
                "collection_name": data["collectionName"],
                "created_at": data["created"],
                "is_dual_audio": data["dualAudio"],
                "files": natsorted(files, alg=ns.PATH),
                "id": data["id"],
                "infohash": infohash,
                "is_best": data["isBest"],
                "release_group": data["releaseGroup"],
                "tracker": tracker,
                "updated_at": data["updated"],
                "url": url,
                "size": size,
            }
            return msgspec.convert(kwargs, type=cls, strict=False)


class EntryRecord(Base, frozen=True, kw_only=True):
    """Represents a single anime entry in SeaDex."""

    anilist_id: int
    """The AniList ID of the anime."""
    collection_id: str
    """The ID of the collection the entry belongs to."""
    collection_name: str
    """The name of the collection the entry belongs to."""
    comparisons: tuple[str, ...]
    """A tuple of comparison urls."""
    created_at: datetime
    """The timestamp of when the entry was created."""
    id: str
    """The ID of the entry."""
    is_incomplete: bool
    """Whether the entry is considered incomplete."""
    notes: str
    """Additional notes about the entry."""
    theoretical_best: str | None
    """The theoretical best release for the entry, if known."""
    torrents: tuple[TorrentRecord, ...]
    """A tuple of `TorrentRecord` objects associated with the entry."""
    updated_at: datetime
    """The timestamp of when the entry was last updated."""
    url: str
    """The URL of the entry."""
    size: int
    """The total size of the entry, calculated by summing the sizes of all files in all torrents."""

    @classmethod
    def from_dict(cls, data: dict[str, Any], /) -> Self:
        """
        Create an instance of this class from a dictionary.

        Parameters
        ----------
        data : dict[str, Any]
            Dictionary representing the instance of this class.

        Returns
        -------
        Self
            An instance of this class.

        """
        try:
            # Attempt a strict conversion, assuming data
            # comes from EntryRecord.to_dict()
            return msgspec.convert(data, type=cls)
        except msgspec.ValidationError:
            # Failed, let's attempt a laxer conversion,
            # assuming the data comes from the SeaDex API.

            # Grab all the torrents in the entry
            # And caclculate the total size of the entry.
            torrents: list[TorrentRecord] = []
            size = 0

            for torrent in data["expand"]["trs"]:
                tr = TorrentRecord.from_dict(torrent)
                size += tr.size
                torrents.append(tr)

            # "comparison" is a comma seperated string,
            # so we'll transform it into a set
            comparisons = {i.strip() for i in data["comparison"].split(",") if i}

            # "theoreticalBest" is an empty string in the API
            # if there's no theoretical best, we'll replace it with None
            theoretical_best = data["theoreticalBest"] if data["theoreticalBest"] else None

            anilist_id = data["alID"]

            kwargs = {
                "anilist_id": anilist_id,
                "collection_id": data["collectionId"],
                "collection_name": data["collectionName"],
                "comparisons": comparisons,
                "created_at": data["created"],
                "id": data["id"],
                "is_incomplete": data["incomplete"],
                "notes": data["notes"],
                "theoretical_best": theoretical_best,
                "updated_at": data["updated"],
                "torrents": torrents,
                "url": f"https://releases.moe/{anilist_id}/",
                "size": size,
            }
            return msgspec.convert(kwargs, type=cls, strict=False)
