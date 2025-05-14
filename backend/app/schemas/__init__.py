# backend/app/schemas/__init__.py

# Re-export enums if they are commonly used or to provide a single import point
# from app.models.enums import UserRoleEnum, UnitTypeEnum, UserCourseRoleEnum

# Re-export commonly used schemas for easier access from other modules (e.g., services, api)

# Common Schemas
from .common_schemas import MsgResponse, PaginatedResponse

# Token Schemas
from .token_schemas import Token, TokenPayload, GoogleIdToken

# User Schemas
from .user_schemas import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserOut,
    UserWithCourses,
    UserForCourseResponse,
    UserRole
)

# Course Schemas
from .course_schemas import (
    CourseBase,
    CourseCreate,
    CourseUpdate,
    CourseOut,
    CourseForUserResponse
)

# Module Schemas
from .module_schemas import (
    ModuleBase,
    ModuleCreate,
    ModuleUpdate,
    ModuleOut
)

# Unit Schemas
from .unit_schemas import (
    UnitBase,
    UnitCreate,
    UnitUpdate,
    UnitOut,
    UnitType
)

# UserCourse (Association) Schemas
from .user_course_schemas import (
    UserCourseBase,
    UserCourseCreate,
    UserCourseUpdate,
    UserCourseOut,
    UserCourseRole
)

# --- Update forward references for Pydantic v2 ---
# Call .model_rebuild() on schemas that use forward references
# or are part of nested structures that might be affected.
# It's generally good to do this for all your main "Out" or response schemas.

UserOut.model_rebuild()
UserWithCourses.model_rebuild()
UserForCourseResponse.model_rebuild()

CourseOut.model_rebuild()
CourseForUserResponse.model_rebuild() # Potentially redundant if UserForCourseResponse is already rebuilt, but safe

ModuleOut.model_rebuild()
UnitOut.model_rebuild() # Though UnitOut might not have forward refs, if it's nested, it's good practice

UserCourseOut.model_rebuild() # If it contains forward refs or complex nested types

# You can also collect all models that might need rebuilding and iterate,
# but explicitly listing them is clear.
# For example:
# all_schemas_to_rebuild = [
#     UserOut, UserWithCourses, UserForCourseResponse,
#     CourseOut, CourseForUserResponse, ModuleOut, UnitOut, UserCourseOut
# ]
# for schema_cls in all_schemas_to_rebuild:
#     try:
#         schema_cls.model_rebuild()
#         print(f"DEBUG: Rebuilt schema: {schema_cls.__name__}")
#     except Exception as e:
#         print(f"ERROR: Failed to rebuild schema {schema_cls.__name__}: {e}")


# If Pydantic v1 was being used, the equivalent would be:
# UserOut.update_forward_refs()
# CourseOut.update_forward_refs()
# ModuleOut.update_forward_refs()
# ... and so on for other models with forward references.
