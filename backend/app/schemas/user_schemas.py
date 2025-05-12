# backend/app/schemas/user_schemas.py
from pydantic import BaseModel, EmailStr, model_validator, ConfigDict
from typing import List, Optional, Any
import enum
import traceback

from app.models.enums import UserRoleEnum as ModelUserRoleEnum
from app.models.user_course import UserCourse as UserCourseORM # For type hinting
from app.models.user import User as UserORM # For type hinting the user object

class UserRole(str, enum.Enum):
    ADMIN = ModelUserRoleEnum.admin.value
    TEACHER = ModelUserRoleEnum.teacher.value
    STUDENT = ModelUserRoleEnum.student.value

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    google_sub: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class UserOut(UserBase):
    id: int

class UserForCourseResponse(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    role: UserRole

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='before')
    @classmethod
    def populate_from_user_course_association(cls, data: Any) -> Any:
        print(f"DEBUG VALIDATOR UserForCourseResponse: Input type: {type(data)}, data: {str(data)[:150]}")
        
        # Check if it's a SQLAlchemy UserCourseORM instance
        if not isinstance(data, UserCourseORM):
            print("DEBUG VALIDATOR UserForCourseResponse: Input not a UserCourseORM instance, passing through.")
            return data

        # Access the related 'user' object. This should trigger lazy load if not already eager loaded.
        # However, selectinload should have handled this.
        user_obj: Optional[UserORM] = getattr(data, 'user', None)
        role_obj = getattr(data, 'role', None) # This is UserCourseRoleEnum

        print(f"DEBUG VALIDATOR UserForCourseResponse: Accessed data.user type: {type(user_obj)}, data.role type: {type(role_obj)}")

        if user_obj is not None and role_obj is not None:
            transformed_data = {
                "id": user_obj.id,
                "email": user_obj.email,
                "name": user_obj.name,
                "role": role_obj.value, # Get the string value from the enum
            }
            print(f"DEBUG VALIDATOR UserForCourseResponse: Successfully transformed: {transformed_data}")
            return transformed_data
        else:
            if user_obj is None:
                print("ERROR VALIDATOR UserForCourseResponse: 'user' attribute on UserCourseORM instance is None or not loaded.")
            if role_obj is None:
                 print("ERROR VALIDATOR UserForCourseResponse: 'role' attribute on UserCourseORM instance is None.")
            # This will lead to Pydantic validation errors for missing fields, which is what we're seeing.
            # It indicates a problem with data loading or the ORM object structure.
            return {} # Return empty dict to force field validation errors if transformation fails

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .course_schemas import CourseForUserResponse

class UserWithCourses(UserOut):
    courses: List["CourseForUserResponse"] = []