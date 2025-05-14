# backend/app/schemas/user_course_schemas.py
from pydantic import BaseModel
from typing import Optional
import uuid
import enum

# Import enums from the models package
from app.models.enums import UserCourseRoleEnum as ModelUserCourseRoleEnum

# Pydantic compatible Enum
class UserCourseRole(str, enum.Enum):
    TEACHER = ModelUserCourseRoleEnum.teacher.value
    STUDENT = ModelUserCourseRoleEnum.student.value
    # Or define directly:
    # TEACHER = "teacher"
    # STUDENT = "student"

# --- Schema for Linking User to Course (Association) ---
class UserCourseBase(BaseModel):
    user_id: int
    course_id: uuid.UUID
    role: UserCourseRole

    class Config:
        from_attributes = True

class UserCourseCreate(UserCourseBase):
    pass

class UserCourseUpdate(BaseModel): # For updating role, for example
    role: Optional[UserCourseRole] = None

class UserCourseOut(UserCourseBase):
    # You can add user and course details here if needed for specific responses,
    # but often the UserOut and CourseOut schemas handle this by nesting.
    # user: "UserOut" # Example, requires forward ref or careful import
    # course: "CourseBase" # Example
    pass