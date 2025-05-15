# backend/app/schemas/module_schemas.py
from pydantic import BaseModel
from typing import List, Optional
import uuid

# Forward references
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .unit_schemas import UnitOut

# --- Base Schema ---
class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: int = 0 # Provide a default

    class Config:
        from_attributes = True

# --- Schema for Creation ---
class ModuleCreate(ModuleBase):
    pass

# --- Schema for Update ---
class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None

# --- Schemas for Output/Response ---
class ModuleOut(ModuleBase):
    id: int
    course_id: uuid.UUID # Include course_id for context
    units: List["UnitOut"] = []

    # Ensure Config is present
    class Config:
        from_attributes = True