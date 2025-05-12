# backend/app/schemas/course_schemas.py
from pydantic import BaseModel, ConfigDict # Import ConfigDict for Pydantic v2
from typing import List, Optional
import uuid

# Assuming UserRole is the Pydantic enum defined in user_schemas.py
from .user_schemas import UserForCourseResponse, UserRole 

# Forward references for nested schemas
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # from .user_schemas import UserForCourseResponse # Already imported above
    from .module_schemas import ModuleOut

class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None

    # Pydantic v2 style configuration
    model_config = ConfigDict(from_attributes=True)

class CourseCreate(CourseBase):
    # Inherits name, description, and model_config from CourseBase
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    # If this schema is also used with from_attributes, add model_config
    # model_config = ConfigDict(from_attributes=True)

class CourseOut(CourseBase): # Inherits name, description, and model_config from CourseBase
    id: uuid.UUID
    
    # --- UNCOMMENTED THESE FIELDS ---
    user_associations: List[UserForCourseResponse] = [] 
    modules: List["ModuleOut"] = [] 
    # --- END UNCOMMENTED ---

    # model_config is inherited from CourseBase, so from_attributes=True is already set.
    # If CourseBase didn't have it, or if you needed to override, you'd add it here:
    # model_config = ConfigDict(from_attributes=True)


class CourseForUserResponse(CourseBase): # Inherits name, description, and model_config
    id: uuid.UUID
    role: UserRole # UserRole should be the Pydantic enum for roles
    modules: List["ModuleOut"] = [] # Optionally include modules here if you want them in this specific response

    # model_config is inherited from CourseBase
