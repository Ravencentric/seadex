from __future__ import annotations

from typing import Iterator

import pytest

from seadex import SeaDex


@pytest.fixture
def seadex_client() -> Iterator[SeaDex]:
    with SeaDex() as seadex:
        yield seadex
