from __future__ import annotations

from os.path import basename
from typing import TYPE_CHECKING
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
        A client to interact with the anime entries in SeaDex.

        Parameters
        ----------
        base_url : str, optional
            The base URL of SeaDex, used for constructing API queries.
        client : Client, optional
            An [`httpx.Client`](https://www.python-httpx.org/api/#client) instance used to make requests to SeaDex.

        Examples
        -------
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
        This is the base URL, used for constructing API queries.
        """
        return self._base_url

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def close(self) -> None:
        """
        Closes the underlying HTTP client connection.
        """
        self._client.close()

    def from_id(self, id: int | str, /) -> EntryRecord:
        """
        Retrieves an entry by its ID.

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
        -------
        EntryNotFoundError
            If no entry is found for the provided ID.
        """
        try:
            if isinstance(id, int):
                params = {"filter": f"alID={id}", "expand": "trs"}  # Anilist IDs are integers
            else:
                params = {"filter": f"id='{id}'", "expand": "trs"}  # Database IDs are strings

            response = self._client.get(self._endpoint, params=params).raise_for_status()
            return EntryRecord._from_dict(response.json()["items"][0])

        except (KeyError, IndexError):
            errmsg = f"No seadex entry found for id: {id}"
            raise EntryNotFoundError(errmsg, response=response)

    def from_title(self, title: str, /) -> EntryRecord:
        """
        Retrieves an entry by its anime title.

        Parameters
        ----------
        title : str
            The title of the anime to search for.

        Returns
        -------
        EntryRecord
            The retrieved entry.

        Raises
        -------
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
            )
            media = response.json()["data"]["Media"]
            anilist_id = media["id"]
            response = self._client.get(
                self._endpoint, params={"filter": f"alID={anilist_id}", "expand": "trs"}
            ).raise_for_status()
            entry_record = EntryRecord._from_dict(response.json()["items"][0])
            setattr(entry_record, "__anilist_title", media["title"]["english"] or media["title"]["romaji"])
            return entry_record

        except (KeyError, IndexError, TypeError):
            errmsg = f"No seadex entry found for title: {title}"
            raise EntryNotFoundError(errmsg, response=response)

    def from_filename(self, filename: StrPath, /) -> Iterator[EntryRecord]:
        """
        Yields entries that may contain a file with the specified filename.

        Parameters
        ----------
        filename : StrPath
            The filename to search for.

        Yields
        -------
        EntryRecord
            The retrieved entry.
        """
        basefilename = basename(filename)
        params = {"filter": f'trs.files?~\'"name":"{basefilename}"\'', "expand": "trs"}
        response = self._client.get(self._endpoint, params=params).raise_for_status()
        for entry in response.json()["items"]:
            yield EntryRecord._from_dict(entry)

    def iterator(self) -> Iterator[EntryRecord]:  # pragma: no cover; Testing this is annoying
        """
        Lazily get all the entries from SeaDex.

        Yields
        ------
        EntryRecord
            The retrieved entry.
        """
        total_pages = (
            self._client.get(self._endpoint, params={"perPage": 500}).raise_for_status().json()["totalPages"] + 1
        )

        for page in range(1, total_pages):
            response = self._client.get(
                self._endpoint, params={"page": page, "perPage": 500, "expand": "trs"}
            ).raise_for_status()
            for item in response.json()["items"]:
                yield EntryRecord._from_dict(item)
