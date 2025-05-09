# backend/app/schemas.py
from pydantic import BaseModel, Field
from enum import Enum as PyEnum
from typing import List, Optional
import uuid # Import Python's uuid module

# --- Enums ---
class Role(str, PyEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class UnitType(str, PyEnum):
    MATERIAL = "material"
    ASSIGNMENT = "assignment"
    QUIZ = "quiz"
    VIDEO = "video"
    DISCUSSION = "discussion"
    EXTERNAL_LINK = "external_link"

# --- Base Schemas ---
class UserBase(BaseModel):
    id: int # User ID remains int
    email: str
    name: Optional[str] = None
    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    id: uuid.UUID # <<<--- CORRECTED TO UUID
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True

class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: Optional[int] = 0
    class Config:
        from_attributes = True

class UnitBase(BaseModel):
    title: str
    unit_type: UnitType = Field(..., alias="type") # Maps to 'type' in JSON
    content: Optional[str] = None
    order: Optional[int] = 0
    class Config:
        from_attributes = True
        populate_by_name = True # Important for alias to work both ways

# --- Schemas for Creation ---
class CourseCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ModuleCreate(ModuleBase):
    # course_id: uuid.UUID # If creating standalone and need to pass course_id
    pass

class UnitCreate(UnitBase):
    # module_id: int # If creating standalone and need to pass module_id
    pass

# --- Schemas for Output ---
class UnitOut(UnitBase):
    id: int

class ModuleOut(ModuleBase):
    id: int
    units: List[UnitOut] = []

class UserForCourseResponse(UserBase):
    role: Role

class CourseOut(CourseBase): # CourseBase now has id: uuid.UUID
    users: List[UserForCourseResponse] = []
    modules: List[ModuleOut] = []

class CourseForUserResponse(CourseBase): # CourseBase now has id: uuid.UUID
    role: Role

class UserOut(UserBase):
    courses: List[CourseForUserResponse] = []

# --- Schemas for Junction Table & Links ---
class UserCourseLink(BaseModel):
    user_id: int
    course_id: uuid.UUID # <<<--- CORRECTED TO UUID
    role: Role
    class Config:
        from_attributes = True

class UserCourseCreate(BaseModel):
    user_id: int
    course_id: uuid.UUID # <<<--- CORRECTED TO UUID
    role: Role