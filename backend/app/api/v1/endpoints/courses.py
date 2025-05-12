# backend/app/api/v1/endpoints/courses.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from typing import List
import traceback # For detailed error logging

from app.db.session import get_db_session # Async DB session
from app.models.user import User as UserModel # SQLAlchemy User model
from app.schemas.course_schemas import CourseOut, CourseCreate # Pydantic schemas
from app.schemas.user_course_schemas import UserCourseCreate, UserCourseOut # For enrollment
from app.api import deps # API dependencies
from app.services.course_service import course_service # Course service layer

router = APIRouter()

@router.get("", response_model=List[CourseOut], summary="List courses for the authenticated user")
@router.get("/", response_model=List[CourseOut], include_in_schema=False) # Keep for flexibility
async def list_my_courses(
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve a list of courses the authenticated user is enrolled in.
    Includes details about the user's role in each course and associated modules/units.
    """
    courses = await course_service.get_courses_for_user(
        db, user=current_user, skip=skip, limit=limit
    )
    # Pydantic should handle the conversion from List[CourseModel] to List[CourseOut]
    # Ensure your CourseOut and nested schemas (UserForCourseResponse, ModuleOut, UnitOut)
    # have `from_attributes = True` in their Config and relationships are correctly loaded by CRUD.
    return courses

@router.get("/{course_id}", response_model=CourseOut, summary="Get a specific course by ID")
async def get_course_details(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Fetch a single course by its ID.
    Includes associated users (with their roles in this course),
    modules (ordered by 'order'), and units (ordered by 'order') within each module.
    """
    print(f"DEBUG: Endpoint /api/v1/courses/{course_id} HIT. Requested by user_id: {current_user.id}")
    try:
        course_orm = await course_service.get_course_by_id_for_user(
            db, course_id=course_id, user=current_user
        )
        if not course_orm:
             print(f"DEBUG: Course service returned None for course_id: {course_id}")
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found by service")

        # --- Start Manual Pydantic Validation for Debugging ---
        print(f"DEBUG [Endpoint]: ORM Course object Name: {course_orm.name}")
        print(f"DEBUG [Endpoint]: ORM Course modules count: {len(course_orm.modules) if course_orm.modules else 0}")
        if course_orm.modules:
            print(f"DEBUG [Endpoint]: ORM First module title: {course_orm.modules[0].title}")
            print(f"DEBUG [Endpoint]: ORM First module units count: {len(course_orm.modules[0].units) if course_orm.modules[0].units else 0}")
            if course_orm.modules[0].units:
                 print(f"DEBUG [Endpoint]: ORM First unit title: {course_orm.modules[0].units[0].title}")
        
        pydantic_course_out_obj = None
        try:
            # This is the critical test for Pydantic serialization from the ORM object
            pydantic_course_out_obj = CourseOut.model_validate(course_orm) # Pydantic v2
            # For Pydantic v1, it would be: pydantic_course_out_obj = CourseOut.from_orm(course_orm)
            
            print(f"DEBUG [Endpoint]: Manually validated Pydantic CourseOut object created.")
            print(f"DEBUG [Endpoint]: Pydantic CourseOut modules count: {len(pydantic_course_out_obj.modules)}")
            print(f"DEBUG [Endpoint]: Pydantic CourseOut user_associations count: {len(pydantic_course_out_obj.user_associations)}")
            # You can print the full object if it's not too large:
            # print(f"DEBUG [Endpoint]: Pydantic CourseOut object (JSON): {pydantic_course_out_obj.model_dump_json(indent=2)}")
        except Exception as e_pydantic_validate:
            print(f"ERROR [Endpoint]: CourseOut.model_validate FAILED: {e_pydantic_validate}")
            traceback.print_exc()
            # If this fails, the problem is definitely with Pydantic schema/config or data shape
            raise HTTPException(status_code=500, detail="Error during Pydantic model validation in endpoint")
        # --- End Manual Pydantic Validation ---

        # If manual validation works and pydantic_course_out_obj has modules/units,
        # but returning course_orm directly to FastAPI still strips them, then
        # the issue is how FastAPI's response_model serialization is working.
        # In that case, you could return the already validated Pydantic object:
        # return pydantic_course_out_obj

        return course_orm # FastAPI will attempt its own model_validate on this using response_model=CourseOut
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in get_course_details endpoint (course_id: {course_id}): {e}")
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error fetching course details.")


@router.post(
    "",
    response_model=CourseOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new course"
)
async def create_new_course(
    course_in: CourseCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Create a new course.
    The user creating the course will automatically be enrolled as a teacher.
    """
    try:
        course = await course_service.create_new_course(
            db, course_data=course_in, creator=current_user
        )
        return course
    except HTTPException:
        raise # Re-raise HTTPExceptions from the service layer
    except Exception as e:
        # Log the error e for server-side debugging
        # print(f"Unexpected error creating course: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the course."
        )

@router.post(
    "/enroll",
    response_model=UserCourseOut, # Schema for the association link
    status_code=status.HTTP_201_CREATED,
    summary="Enroll a user in a course"
)
async def enroll_user_in_course_endpoint( # Renamed to avoid conflict
    enrollment_data: UserCourseCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(deps.get_current_active_user) # For authorization checks
):
    """
    Enroll a user into a specific course with a given role.
    Authorization logic (e.g., only admins/teachers can enroll others) can be in the service.
    """
    try:
        user_course_link = await course_service.enroll_new_user_in_course(
            db, enrollment_data=enrollment_data, current_user=current_user
        )
        return user_course_link
    except HTTPException:
        raise # Re-raise HTTPExceptions from the service layer
    except Exception as e:
        # Log the error e
        # print(f"Unexpected error enrolling user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while enrolling the user."
        )