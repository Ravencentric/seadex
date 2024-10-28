from __future__ import annotations

from typing import Iterator

import pytest

from seadex import SeaDexEntry


@pytest.fixture
def seadex_entry() -> Iterator[SeaDexEntry]:
    with SeaDexEntry() as seadex:
        yield seadex
