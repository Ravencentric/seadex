from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from seadex import SeaDexBackup, SeaDexEntry

if TYPE_CHECKING:
    from collections.abc import Iterator

    from pytest_httpx import HTTPXMock


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
