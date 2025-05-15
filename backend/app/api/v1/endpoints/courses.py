# backend/app/api/v1/endpoints/courses.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from typing import List
import traceback
from app.db.session import get_db_session
from app.models.user import User as UserModel
from app.schemas.course_schemas import CourseOut, CourseCreate
from app.schemas.user_course_schemas import UserCourseCreate, UserCourseOut
from app.api import deps
from app.services.course_service import course_service

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
        
        pydantic_course_out_obj = None
        try:
            pydantic_course_out_obj = CourseOut.model_validate(course_orm) # Pydantic v2
            
        except Exception as e_pydantic_validate:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Error during Pydantic model validation in endpoint")

        return course_orm
    
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
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the course."
        )

@router.post(
    "/enroll",
    response_model=UserCourseOut,
    status_code=status.HTTP_201_CREATED,
    summary="Enroll a user in a course"
)
async def enroll_user_in_course_endpoint(
    enrollment_data: UserCourseCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(deps.get_current_active_user)
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
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while enrolling the user."
        )