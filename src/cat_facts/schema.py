from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .config import cat_facts_config as cfg

class CatFactBase(BaseModel):
    fact: str = Field(
        ...,
        min_length=cfg.min_fact_length,
        max_length=cfg.max_fact_length,
        description="Fact about cats"
    )
    length: int = Field(
        ...,
        ge=cfg.min_fact_count,
        le=cfg.max_fact_count,
        description="Length of the fact"
    )

class CatFactCreate(CatFactBase):
    pass

class CatFactUpdate(CatFactBase):
    fact: Optional[str] = Field(None, min_length=cfg.min_fact_length, max_length=cfg.max_fact_length)
    length: Optional[int] = Field(None, ge=cfg.min_fact_count, le=cfg.max_fact_count)

class CatFactResponse(CatFactBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CatFactStatsResponse(BaseModel):
    total_facts: int
    average_length: float
    longest_fact: int
    shortest_fact: int

    class Config:
        from_attributes = True
