from pydantic import BaseModel
from enum import Enum as PyEnum # Python's enum, aliased to avoid confusion if you import SQLA Enum
from typing import List, Optional

# 1. Define the Role Enum (matches UserRoleEnum in models.py)
class Role(str, PyEnum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

# 2. Base schemas for User and Course
class UserBase(BaseModel):
    id: int
    email: str
    name: Optional[str] = None # Match model where name is nullable

    class Config:
        orm_mode = True

class CourseBase(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True

# 3. Schemas for representing the relationship in nested structures

# Represents a user linked to a course, including their role in that course.
class UserForCourseResponse(UserBase):
    role: Role

# Represents a course linked to a user, including the user's role in that course.
class CourseForUserResponse(CourseBase):
    role: Role

# 4. Main output schemas
class UserOut(UserBase):
    # List of courses the user is associated with, including their role in each.
    # This will be populated from User.course_associations
    courses: List[CourseForUserResponse] = []

    class Config:
        orm_mode = True # Ensure this is here if not inherited properly or if UserBase doesn't have it

class CourseOut(CourseBase):
    # List of users associated with the course, including their role in this course.
    # This will be populated from Course.user_associations
    users: List[UserForCourseResponse] = []

    class Config:
        orm_mode = True # Ensure this is here

# 5. Schema for the junction table link (UserCourse) - useful for direct operations or debugging
class UserCourseLink(BaseModel):
    user_id: int
    course_id: int
    role: Role

    class Config:
        orm_mode = True

# Schema for creating a link (e.g., enrolling a user in a course)
class UserCourseCreate(BaseModel):
    user_id: int
    course_id: int
    role: Role
