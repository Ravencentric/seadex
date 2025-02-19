from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class FrozenBaseModel(BaseModel):
    """Frozen pydantic.BaseModel."""

    model_config = ConfigDict(frozen=True)
