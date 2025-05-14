# backend/app/schemas/unit_schemas.py
from pydantic import BaseModel, Field
from typing import Optional
import enum

# Import enums from the models package
from app.models.enums import UnitTypeEnum as ModelUnitTypeEnum

# Pydantic compatible Enum
class UnitType(str, enum.Enum):
    MATERIAL = ModelUnitTypeEnum.MATERIAL.value
    ASSIGNMENT = ModelUnitTypeEnum.ASSIGNMENT.value
    QUIZ = ModelUnitTypeEnum.QUIZ.value
    VIDEO = ModelUnitTypeEnum.VIDEO.value
    DISCUSSION = ModelUnitTypeEnum.DISCUSSION.value
    EXTERNAL_LINK = ModelUnitTypeEnum.EXTERNAL_LINK.value
    # Or define directly:
    # MATERIAL = "material"
    # ASSIGNMENT = "assignment"
    # QUIZ = "quiz"
    # VIDEO = "video"
    # DISCUSSION = "discussion"
    # EXTERNAL_LINK = "external_link"

# --- Base Schema ---
class UnitBase(BaseModel):
    title: str
    # The alias "type" means that in the JSON payload, this field will be "type",
    # but in your Pydantic model, it's accessed as "unit_type".
    unit_type: UnitType = Field(..., alias="type")
    content: Optional[str] = None # Could be JSON for more structured content
    order: int = 0 # Provide a default

    class Config:
        from_attributes = True
        populate_by_name = True # Allows populating by field name OR alias

# --- Schema for Creation ---
class UnitCreate(UnitBase):
    module_id: Optional[int] = None # Usually set via path or service logic

# --- Schema for Update ---
class UnitUpdate(BaseModel):
    title: Optional[str] = None
    unit_type: Optional[UnitType] = Field(default=None, alias="type")
    content: Optional[str] = None
    order: Optional[int] = None

# --- Schemas for Output/Response ---
class UnitOut(UnitBase):
    id: int
    module_id: int # Include module_id for context