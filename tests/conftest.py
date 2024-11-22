from __future__ import annotations

from collections.abc import Iterator

import pytest
from pytest_httpx import HTTPXMock

from seadex import SeaDexBackup, SeaDexEntry


@pytest.fixture
def seadex_entry() -> Iterator[SeaDexEntry]:
    with SeaDexEntry() as seadex:
        yield seadex


@pytest.fixture
def seadex_backup(httpx_mock: HTTPXMock) -> Iterator[SeaDexBackup]:
    httpx_mock.add_response(url="https://releases.moe/api/admins/auth-with-password", json={"token": "secret"})
    httpx_mock.add_response(
        url="https://releases.moe/api/files/token", json={"token": "secret"}, is_reusable=True, is_optional=True
    )
    with SeaDexBackup("me@example.com", "example") as seadex:
        yield seadex
