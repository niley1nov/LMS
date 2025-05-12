from pydantic import BaseModel
from typing import Optional, TypeVar, Generic, List

DataT = TypeVar('DataT')

class MsgResponse(BaseModel):
    """
    Generic message response schema.
    """
    msg: str
    detail: Optional[str] = None

class PaginatedResponse(BaseModel, Generic[DataT]):
    """
    Generic paginated response schema.
    """
    total: int
    page: int
    size: int
    data: List[DataT]
    # has_next: bool
    # has_prev: bool