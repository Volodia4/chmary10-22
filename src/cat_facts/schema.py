from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from .config import cat_facts_config as cfg


class CatFactBase(BaseModel):
    fact: str = Field(
        ...,
        min_length=cfg.min_fact_length,
        max_length=cfg.max_fact_length,
        description="Interesting fact about cats"
    )
    length: int = Field(
        ...,
        ge=cfg.min_length_value,
        le=cfg.max_length_value,
        description="Length of the fact text"
    )
    source: Optional[str] = Field("catfact.ninja", description="Source of the fact")


class CatFactCreate(CatFactBase):
    pass


class CatFactUpdate(BaseModel):
    fact: Optional[str] = Field(
        None,
        min_length=cfg.min_fact_length,
        max_length=cfg.max_fact_length
    )
    length: Optional[int] = Field(
        None,
        ge=cfg.min_length_value,
        le=cfg.max_length_value
    )


class CatFactResponse(CatFactBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CatFactListResponse(BaseModel):
    items: list[CatFactResponse]
    total: int
    page: int
    size: int
