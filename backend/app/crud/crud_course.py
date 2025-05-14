# backend/app/crud/crud_course.py
from typing import List, Optional, Union, Dict, Any, Type
import uuid
import traceback

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload

from app.crud.base_crud import CRUDBase
from app.models.course import Course as CourseModel
from app.models.user_course import UserCourse as UserCourseModel
from app.models.user import User as UserModel
from app.models.module_model import Module as ModuleModel
from app.models.unit import Unit as UnitModel
from app.schemas.course_schemas import CourseCreate, CourseUpdate
from app.schemas.user_course_schemas import UserCourseRole

class CRUDCourse(CRUDBase[CourseModel, CourseCreate, CourseUpdate]):
    def __init__(self, model: Type[CourseModel]):
        super().__init__(model)
        # Use builtins.id() if you ever shadow 'id' locally and need the built-in
        # import builtins as bltns
        print(f"DEBUG: CRUDCourse instance {id(self)} initialized with model: {model.__name__}")

    # ... (get_multi_for_user method remains the same) ...
    async def get_multi_for_user(
        self, db: AsyncSession, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[CourseModel]:
        print(f"DEBUG: CRUDCourse.get_multi_for_user called for user_id: {user_id}")
        stmt = (
            select(self.model)
            .join(UserCourseModel, self.model.id == UserCourseModel.course_id)
            .filter(UserCourseModel.user_id == user_id)
            .options(
                selectinload(self.model.user_associations).joinedload(UserCourseModel.user),
                selectinload(self.model.modules).selectinload(ModuleModel.units)
            )
            .offset(skip)
            .limit(limit)
            .order_by(self.model.name)
        )
        result = await db.execute(stmt)
        courses = result.scalars().unique().all()
        print(f"DEBUG: CRUDCourse.get_multi_for_user found {len(courses)} courses")
        return courses

    async def get_with_details(self, db: AsyncSession, *, course_uuid: uuid.UUID) -> Optional[CourseModel]: # Renamed 'id' to 'course_uuid'
        """
        Get a single course by ID with all its details:
        user associations (and their users), modules (and their units).
        """
        # Use builtins.id() if 'id' is ever shadowed in this scope and you need the function
        # import builtins as bltns
        print(f"DEBUG: ***** ENTERING CRUDCourse.get_with_details (instance {id(self)}) for course_uuid: {course_uuid} *****")
        try:
            stmt = (
                select(self.model)
                .options(
                    selectinload(self.model.user_associations).selectinload(UserCourseModel.user),
                    selectinload(self.model.modules).selectinload(ModuleModel.units)
                )
                .filter(self.model.id == course_uuid) # Use renamed parameter course_uuid
            )
            print(f"DEBUG: CRUDCourse.get_with_details - Executing statement: {str(stmt)}")
            result = await db.execute(stmt)
            course = result.scalars().first()

            if course:
                print(f"DEBUG: Course found by SQLAlchemy: ID {course.id}, Name: {course.name!r}")
                if hasattr(course, 'user_associations'):
                    print(f"DEBUG: Number of user_associations loaded: {len(course.user_associations) if course.user_associations is not None else 'Attribute exists but is None'}")
                    if course.user_associations:
                        for i, assoc in enumerate(course.user_associations):
                            user_info = "User object not loaded"
                            if hasattr(assoc, 'user') and assoc.user:
                                user_info = f"ID {assoc.user.id}, Email {assoc.user.email!r}"
                            print(f"  Assoc {i+1}: User ID FK: {assoc.user_id}, Role: {assoc.role.value if assoc.role else 'N/A'}, {user_info}")
                else:
                    print("DEBUG: 'user_associations' attribute NOT FOUND on course object.")

                if hasattr(course, 'modules'):
                    print(f"DEBUG: Number of modules loaded: {len(course.modules) if course.modules is not None else 'Attribute exists but is None'}")
                    if course.modules:
                        for i, module_obj in enumerate(course.modules):
                            print(f"  Module {i+1}: ID {module_obj.id}, Title: {module_obj.title!r}, Order: {module_obj.order}")
                            if hasattr(module_obj, 'units'):
                                print(f"    DEBUG: Number of units in module {module_obj.id}: {len(module_obj.units) if module_obj.units is not None else 'Attribute exists but is None'}")
                                if module_obj.units:
                                    for j, unit_obj in enumerate(module_obj.units):
                                        unit_type_val = "N/A"
                                        if hasattr(unit_obj, 'unit_type') and unit_obj.unit_type:
                                            unit_type_val = unit_obj.unit_type.value
                                        print(f"      Unit {j+1}: ID {unit_obj.id}, Title: {unit_obj.title!r}, Type: {unit_type_val}, Order: {unit_obj.order}")
                            else:
                                print(f"    DEBUG: 'units' attribute NOT FOUND on module {module_obj.id}.")
                else:
                    print("DEBUG: 'modules' attribute NOT FOUND on course object.")
            else:
                print(f"DEBUG: Course with ID {course_uuid} not found in DB by SQLAlchemy.")
            
            print(f"DEBUG: ***** EXITING CRUDCourse.get_with_details - Returning course object: {'Exists' if course else 'None'} *****")
            return course
        except Exception as e:
            print(f"ERROR in CRUDCourse.get_with_details (course_uuid: {course_uuid}): {e}")
            traceback.print_exc()
            return None

    async def enroll_user(
        self, db: AsyncSession, *, user_id: int, course_id: uuid.UUID, role: UserCourseRole # Changed course_id to course_uuid if used internally
    ) -> Union[UserCourseModel, str, None]:
        print(f"DEBUG: CRUDCourse.enroll_user called: user_id={user_id}, course_id={course_id}, role={role.value}")
        # Using course_id as it's specific to the UserCourseModel context
        user_exists_stmt = select(UserModel).filter_by(id=user_id)
        user_res = await db.execute(user_exists_stmt)
        if not user_res.scalars().first():
            return "user_not_found"

        # Using self.get (from CRUDBase) which expects 'record_id' if we were to use it here for course
        # For consistency, let's use a direct select for course existence check
        course_exists_stmt = select(CourseModel).filter_by(id=course_id) # Use course_id for this specific query
        course_res = await db.execute(course_exists_stmt)
        if not course_res.scalars().first():
            return "course_not_found"

        existing_stmt = select(UserCourseModel).filter_by(user_id=user_id, course_id=course_id)
        existing_result = await db.execute(existing_stmt)
        if existing_result.scalars().first():
            return "already_exists"

        db_user_course = UserCourseModel(
            user_id=user_id,
            course_id=course_id,
            role=role
        )
        db.add(db_user_course)
        await db.commit()
        await db.refresh(db_user_course)
        await db.refresh(db_user_course, attribute_names=["user", "course"])
        return db_user_course

    async def create_course_with_creator_enrollment(
        self, db: AsyncSession, *, obj_in: CourseCreate, creator_id: int, creator_role: UserCourseRole
    ) -> CourseModel:
        print(f"DEBUG: CRUDCourse.create_course_with_creator_enrollment called by creator_id: {creator_id}")
        db_course_data = obj_in.model_dump()
        db_course = self.model(**db_course_data)
        db.add(db_course)
        await db.flush()

        user_course_association = UserCourseModel(
            user_id=creator_id,
            course_id=db_course.id,
            role=creator_role
        )
        db.add(user_course_association)
        await db.commit()
        
        refreshed_course = await self.get_with_details(db, course_uuid=db_course.id) # Use course_uuid
        print(f"DEBUG: Course created and refreshed with details: ID {refreshed_course.id if refreshed_course else db_course.id}")
        return refreshed_course if refreshed_course else db_course

crud_course = CRUDCourse(CourseModel)
print(f"DEBUG: crud_course instance (ID: {id(crud_course)}) created in crud_course.py with model {CourseModel.__name__}")
