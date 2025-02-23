from __future__ import annotations

import re
from os.path import basename
from typing import TYPE_CHECKING, Any
from urllib.parse import urljoin

from seadex._exceptions import EntryNotFoundError
from seadex._records import EntryRecord
from seadex._types import StrPath
from seadex._utils import httpx_client

if TYPE_CHECKING:
    from collections.abc import Iterator

    from httpx import Client
    from typing_extensions import Self


class SeaDexEntry:
    def __init__(self, base_url: str = "https://releases.moe", client: Client | None = None) -> None:
        """
        Client to interact with SeaDex entries.

        Parameters
        ----------
        base_url : str, optional
            The base URL of SeaDex, used for constructing API queries.
        client : Client, optional
            An [httpx.Client][] instance used to make requests to SeaDex.

            [httpx.Client]: https://www.python-httpx.org/advanced/#client

        Examples
        --------
        ```py
        with SeaDexEntry() as entry:
            tamako = entry.from_title("tamako love story")
            for torrent in tamako.torrents:
                if torrent.is_best and torrent.tracker.is_public():
                    print(torrent.release_group)
                    #> LYS1TH3A
                    #> Okay-Subs
        ```

        """
        self._base_url = base_url
        self._endpoint = urljoin(self._base_url, "/api/collections/entries/records")
        self._client = httpx_client() if client is None else client

    @property
    def base_url(self) -> str:
        """
        Base URL, used for constructing API queries.
        """
        return self._base_url

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def __from_filter(self, filter: str | None, /, *, paginate: bool) -> Iterator[EntryRecord]:
        """Yield entries that match the provided filter."""
        params: dict[str, Any] = {}

        if filter is None:
            params.update({"perPage": 500, "expand": "trs"})
        else:
            params.update({"perPage": 500, "expand": "trs", "filter": filter})

        if paginate:
            first_page = self._client.get(self._endpoint, params=params).raise_for_status()
            data = first_page.json()
            total_pages = data["totalPages"]

            for item in data["items"]:  # Page 1
                yield EntryRecord._from_dict(item)

            for page in range(2, total_pages + 1):  # Page 2 to total_pages
                params.update({"page": page})
                response = self._client.get(self._endpoint, params=params).raise_for_status()
                for item in response.json()["items"]:
                    yield EntryRecord._from_dict(item)
        else:
            params.update({"skipTotal": True})
            response = self._client.get(self._endpoint, params=params).raise_for_status()
            for item in response.json()["items"]:
                yield EntryRecord._from_dict(item)

    def close(self) -> None:
        """
        Close the underlying HTTP client connection.
        """
        self._client.close()

    def from_filter(self, filter: str, /) -> Iterator[EntryRecord]:
        """
        Yield entries from SeaDex that match the given filter expression.

        Refer to the `filter` argument in the [PocketBase API documentation][]
        for details on constructing valid filter expressions.

        [PocketBase API documentation]: https://pocketbase.io/docs/api-records/#listsearch-records

        Parameters
        ----------
        filter : str
            The filter expression.

        Yields
        ------
        EntryRecord
            The retrieved entry.

        Raises
        ------
        TypeError
            If `filter` is not a string.

        """
        if not isinstance(filter, str):
            errmsg = f"'filter' must be a string, not {type(filter).__name__}."
            raise TypeError(errmsg)

        yield from self.__from_filter(filter, paginate=True)

    def from_id(self, id: int | str, /) -> EntryRecord:
        """
        Retrieve an entry by its ID.

        Parameters
        ----------
        id : int | str
            The ID of the entry. Can be an AniList ID (integer)
            or a SeaDex database ID (string).

        Returns
        -------
        EntryRecord
            The retrieved entry.

        Raises
        ------
        EntryNotFoundError
            If no entry is found for the provided ID.

        """
        filter = f"alID={id}" if isinstance(id, int) else f"id='{id}'"
        entries = self.__from_filter(filter, paginate=False)

        try:
            return next(entries)
        except StopIteration:
            errmsg = f"No seadex entry found for id: {id}"
            raise EntryNotFoundError(errmsg) from None

    def from_title(self, title: str, /) -> EntryRecord:
        """
        Retrieve an entry by its anime title.

        Parameters
        ----------
        title : str
            The title of the anime to search for.

        Returns
        -------
        EntryRecord
            The retrieved entry.

        Raises
        ------
        EntryNotFoundError
            If no entry is found for the provided title.

        """
        try:
            response = self._client.post(
                "https://graphql.anilist.co",
                json={
                    "query": "query ($search: String!) { Media(search: $search, type: ANIME) { id title { english romaji } } }",
                    "variables": {"search": title},
                },
            ).raise_for_status()

            media = response.json()["data"]["Media"]
            anilist_id = media["id"]

            entries = self.__from_filter(f"alID={anilist_id}", paginate=False)
            entry_record = next(entries)
            entry_record._anilist_title = media["title"]["english"] or media["title"]["romaji"]  # type: ignore[attr-defined]
            return entry_record

        except (StopIteration, TypeError):
            errmsg = f"No seadex entry found for title: {title}"
            raise EntryNotFoundError(errmsg) from None

    def from_filename(self, filename: StrPath, /) -> Iterator[EntryRecord]:
        """
        Yield entries that contain a torrent with the specified filename.

        Parameters
        ----------
        filename : StrPath
            The filename to search for.

        Yields
        ------
        EntryRecord
            The retrieved entry.

        """
        yield from self.__from_filter(f'trs.files?~\'"name":"{basename(filename)}"\'', paginate=False)

    def from_infohash(self, infohash: str, /) -> Iterator[EntryRecord]:
        """
        Yield entries that contain a torrent with the specified infohash.

        Parameters
        ----------
        infohash : str
            The infohash to search for.

        Yields
        ------
        EntryRecord
            The retrieved entry.

        Raises
        ------
        TypeError
            If `infohash` is not a string.
        ValueError
            If `infohash` is not a 40-character hexadecimal string.

        """
        if not isinstance(infohash, str):
            errmsg = f"'infohash' must be a string, not {type(infohash).__name__}."
            raise TypeError(errmsg)

        infohash = infohash.lower().strip()

        if not re.match(r"^[0-9a-f]{40}$", infohash):
            errmsg = "Invalid infohash format. Must be a 40-character hexadecimal string."
            raise ValueError(errmsg)

        yield from self.__from_filter(f"trs.infoHash?='{infohash}'", paginate=False)

    def iterator(self) -> Iterator[EntryRecord]:
        """
        Lazily iterate over all the entries in SeaDex.

        Yields
        ------
        EntryRecord
            The retrieved entry.

        """
        yield from self.__from_filter(None, paginate=True)
