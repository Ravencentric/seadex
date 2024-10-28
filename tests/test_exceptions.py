from __future__ import annotations

import pytest
from pytest_httpx import HTTPXMock

from seadex import EntryNotFoundError, SeaDex


def test_entry_not_found_from_anilist_id(seadex_client: SeaDex, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?filter=alID=98329837198378237183918&expand=trs",
        json={"page": 1, "perPage": 30, "totalItems": 0, "totalPages": 0, "items": []},
    )

    with pytest.raises(EntryNotFoundError):
        seadex_client.from_id(98329837198378237183918)


def test_entry_not_found_from_seadex_id(seadex_client: SeaDex, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://releases.moe/api/collections/entries/records?filter=id='jashdsjhdsakjdhsakdhsadhaksjd'&expand=trs",
        json={"page": 1, "perPage": 30, "totalItems": 0, "totalPages": 0, "items": []},
    )

    with pytest.raises(EntryNotFoundError):
        seadex_client.from_id("jashdsjhdsakjdhsakdhsadhaksjd")


def test_entry_not_found_from_title(seadex_client: SeaDex, httpx_mock: HTTPXMock) -> None:
    httpx_mock.add_response(
        url="https://graphql.anilist.co",
        json={
            "errors": [{"message": "Not Found.", "status": 404, "locations": [{"line": 1, "column": 28}]}],
            "data": {"Media": None},
        },
    )

    with pytest.raises(EntryNotFoundError):
        seadex_client.from_title("jashdsjhdsakjdhsakdhsadhaksjd")
