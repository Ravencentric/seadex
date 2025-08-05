from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from seadex import SeaDexBackup, SeaDexEntry

if TYPE_CHECKING:
    from collections.abc import Iterator

    from pytest_httpx import HTTPXMock


@pytest.fixture
def sample_response() -> dict[str, Any]:
    file = Path(__file__).resolve().parent / "sample_response.json"
    with open(file, encoding="utf-8") as f:
        return json.load(f)  # type: ignore[no-any-return]


@pytest.fixture
def seadex_entry(sample_response: dict[str, Any]) -> Iterator[SeaDexEntry]:
    @dataclass
    class MockResponse:
        data: dict[str, Any]

        def json(self) -> dict[str, Any]:
            return self.data

        def raise_for_status(self) -> MockResponse:
            return self

    @dataclass
    class MockClient:
        def get(self, *args: Any, **kwargs: Any) -> MockResponse:
            return MockResponse(sample_response)

        def post(self, url: str, *args: Any, **kwargs: Any) -> MockResponse:
            if url == "https://graphql.anilist.co":
                return MockResponse(
                    {
                        "data": {
                            "Media": {
                                "id": 165790,
                                "title": {
                                    "english": "365 Days to the Wedding",
                                    "romaji": "Kekkon Suru tte, Hontou desu ka",
                                },
                            }
                        }
                    }
                )
            msg = f"Unexpected URL: {url}"  # pragma: no cover
            raise ValueError(msg)  # pragma: no cover

        def close(self) -> None:
            pass

    with SeaDexEntry(client=MockClient()) as seadex:  # type: ignore[arg-type]
        yield seadex


@pytest.fixture
def seadex_backup(httpx_mock: HTTPXMock) -> Iterator[SeaDexBackup]:
    httpx_mock.add_response(url="https://releases.moe/api/admins/auth-with-password", json={"token": "secret"})
    httpx_mock.add_response(
        url="https://releases.moe/api/files/token", json={"token": "secret"}, is_reusable=True, is_optional=True
    )
    with SeaDexBackup("me@example.com", "example") as seadex:
        yield seadex
