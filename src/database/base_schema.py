from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, Optional
from datetime import datetime

T = TypeVar('T')

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class BaseResponseSchema(BaseSchema):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int
