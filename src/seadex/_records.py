from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin

from natsort import natsorted, ns
from pydantic import ByteSize, ValidationInfo, field_validator

from seadex._enums import Tracker
from seadex._models import FrozenBaseModel
from seadex._torrent import File
from seadex._types import UTCDateTime

if TYPE_CHECKING:
    from typing_extensions import Self


class TorrentRecord(FrozenBaseModel):
    """Represents a single torrent record within a SeaDex entry."""

    collection_id: str
    """The ID of the collection the torrent record belongs to."""
    collection_name: str
    """The name of the collection the torrent record belongs to."""
    created_at: UTCDateTime
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
    updated_at: UTCDateTime
    """The timestamp of when the torrent record was last updated."""
    url: str
    """The URL of the torrent."""

    @cached_property
    def size(self) -> ByteSize:
        """The total size of the torrent, calculated by summing the sizes of all files."""
        return ByteSize(sum(f.size for f in self.files))

    @classmethod
    def _from_dict(cls, dictionary: dict[str, Any], /) -> Self:
        """Parse the response from the SeaDex API into a `TorrentRecord` object."""
        kwargs = {
            "collection_id": dictionary["collectionId"],
            "collection_name": dictionary["collectionName"],
            "created_at": dictionary["created"],
            "is_dual_audio": dictionary["dualAudio"],
            "files": ({"name": file["name"], "size": file["length"]} for file in dictionary["files"]),
            "id": dictionary["id"],
            "infohash": dictionary["infoHash"],
            "is_best": dictionary["isBest"],
            "release_group": dictionary["releaseGroup"],
            "tracker": dictionary["tracker"],
            "updated_at": dictionary["updated"],
            "url": dictionary["url"],
        }
        return cls.model_validate(kwargs)

    @field_validator("infohash")
    @classmethod
    def _replace_placeholder_infohash(cls, value: str) -> str | None:
        """
        SeaDex API uses `<redacted>` to indicate that the torrent has no infohash (because it's private).
        This replaces it with None for a more pythonic approach.
        """
        if value.strip().casefold() == "<redacted>":  # Private torrents do not have an infohash
            return None
        return value

    @field_validator("files")
    @classmethod
    def _sort_files(cls, value: tuple[File, ...]) -> tuple[File, ...]:
        """Sort the files."""
        return tuple(natsorted(value, key=lambda file: file.name, alg=ns.PATH))

    @field_validator("url", mode="after")
    @classmethod
    def _resolve_url(cls, value: str, info: ValidationInfo) -> str:
        tracker: Tracker = info.data["tracker"]

        if not value.startswith(tracker.url):
            return urljoin(tracker.url, value)
        return value


class EntryRecord(FrozenBaseModel):
    """Represents a single anime entry in SeaDex."""

    anilist_id: int
    """The AniList ID of the anime."""
    collection_id: str
    """The ID of the collection the entry belongs to."""
    collection_name: str
    """The name of the collection the entry belongs to."""
    comparisons: tuple[str, ...]
    """A tuple of comparison urls."""
    created_at: UTCDateTime
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
    updated_at: UTCDateTime
    """The timestamp of when the entry was last updated."""

    @property
    def url(self) -> str:
        """The URL of the entry."""
        return f"https://releases.moe/{self.anilist_id}/"

    @classmethod
    def _from_dict(cls, dictionary: dict[str, Any], /) -> Self:
        """Parse the response from the SeaDex API into a `EntryRecord` object."""
        kwargs = {
            "anilist_id": dictionary["alID"],
            "collection_id": dictionary["collectionId"],
            "collection_name": dictionary["collectionName"],
            "comparisons": (i.strip() for i in dictionary["comparison"].split(",") if i != ""),
            "created_at": dictionary["created"],
            "id": dictionary["id"],
            "is_incomplete": dictionary["incomplete"],
            "notes": dictionary["notes"],
            "theoretical_best": dictionary["theoreticalBest"],
            "updated_at": dictionary["updated"],
            "torrents": [TorrentRecord._from_dict(tr) for tr in dictionary["expand"]["trs"]],
        }
        return cls.model_validate(kwargs)

    @field_validator("theoretical_best")
    @classmethod
    def _replace_placeholder_infohash(cls, value: str) -> str | None:
        """
        SeaDex API uses an empty string to indicate an empty theoreticalBest field.
        This replaces it with None for a more pythonic approach.
        """
        return value if value else None
