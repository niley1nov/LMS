# File: backend/app/routes/courses.py
from fastapi import APIRouter, Depends, HTTPException # Query removed if target_user_id is removed
from sqlalchemy.orm import Session, joinedload, selectinload
from typing import List # Optional removed if target_user_id is removed

from ..database import SessionLocal
from .. import models
from .. import schemas
from ..deps import get_current_user # This is key

router = APIRouter(prefix="/courses", tags=["courses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modified to fetch courses for the authenticated user
@router.get("", response_model=List[schemas.CourseOut]) # Matches /courses
@router.get("/", response_model=List[schemas.CourseOut]) # Keep for flexibility
def list_my_courses( # Consider renaming if you prefer, e.g. list_my_courses
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # User from session/token
):
    # Use the ID of the currently authenticated user to filter courses
    user_id_to_filter_by = current_user.get("sub")

    # Query courses associated with the current_user
    query = db.query(models.Course)\
              .join(models.UserCourse, models.Course.id == models.UserCourse.course_id)\
              .filter(models.UserCourse.user_id == user_id_to_filter_by)
    
    # Eagerly load user_associations and the associated user.
    # This helps in constructing the 'users' field in CourseOut efficiently.
    query = query.options(
        selectinload(models.Course.user_associations).joinedload(models.UserCourse.user)
    )
    
    db_courses = query.all()
    
    result_courses = []
    for course in db_courses:
        # For each course, the 'users' list in CourseOut will contain
        # the current_user's information regarding their role in this specific course.
        # This maintains consistency with your previous logic where target_user_id shaped this.
        user_info_for_course = None
        for assoc in course.user_associations:
            if assoc.user_id == user_id_to_filter_by: # We are interested in the current user's role
                user_info_for_course = schemas.UserForCourseResponse(
                    id=assoc.user.id,
                    email=assoc.user.email,
                    name=assoc.user.name,
                    role=assoc.role.value # Use .value to get the string from enum
                )
                break # Found the current user's association for this course
        
        # The main query already ensures the course is related to user_id_to_filter_by.
        # So, user_info_for_course should ideally always be found.
        users_list_for_response = [user_info_for_course] if user_info_for_course else []

        result_courses.append(schemas.CourseOut(
            id=course.id,
            name=course.name,
            description=course.description,
            users=users_list_for_response # Contains only current user's details for this course
        ))
    return result_courses


# The GET /{course_id} endpoint can remain largely the same.
# It fetches a specific course and lists all users associated with it.
# The `current_user` dependency ensures that the user is authenticated
# to access this endpoint (you might add more specific authorization logic later if needed).
@router.get("/{course_id}", response_model=schemas.CourseOut)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Auth check
):
    course = db.query(models.Course)\
        .options(selectinload(models.Course.user_associations).joinedload(models.UserCourse.user))\
        .filter(models.Course.id == course_id)\
        .first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if the current user is actually part of this course if that's a requirement
    # For example:
    # if not any(assoc.user_id == current_user.id for assoc in course.user_associations):
    #     raise HTTPException(status_code=403, detail="Not authorized to view this course details")
    # This is an optional, more granular authorization step.

    users_for_course = []
    for assoc in course.user_associations:
        users_for_course.append(schemas.UserForCourseResponse(
            id=assoc.user.id,
            email=assoc.user.email,
            name=assoc.user.name,
            role=assoc.role.value
        ))
    
    return schemas.CourseOut(
        id=course.id,
        name=course.name,
        description=course.description,
        users=users_for_course # Lists all users for this specific course
    )

# POST /enroll endpoint can remain as is, current_user can be used for authorization
# (e.g. only an admin or teacher can enroll others, or users can enroll themselves)
@router.post("/enroll", response_model=schemas.UserCourseLink, status_code=201)
def enroll_user_in_course(
    enrollment: schemas.UserCourseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Example authorization: Only allow users to enroll themselves, unless they are admin
    # if enrollment.user_id != current_user.id and not current_user.is_admin: # Assuming an is_admin flag
    #     raise HTTPException(status_code=403, detail="Not authorized to enroll this user")

    db_user = db.query(models.User).filter(models.User.id == enrollment.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User with id {enrollment.user_id} not found")
    
    db_course = db.query(models.Course).filter(models.Course.id == enrollment.course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail=f"Course with id {enrollment.course_id} not found")

    existing_association = db.query(models.UserCourse).filter(
        models.UserCourse.user_id == enrollment.user_id,
        models.UserCourse.course_id == enrollment.course_id
    ).first()

    if existing_association:
        raise HTTPException(
            status_code=409,
            detail=f"User {enrollment.user_id} is already associated with course {enrollment.course_id}. "
                   f"Current role: {existing_association.role.value}."
        )

    db_user_course = models.UserCourse(
        user_id=enrollment.user_id,
        course_id=enrollment.course_id,
        role=enrollment.role
    )
    db.add(db_user_course)
    db.commit()
    db.refresh(db_user_course)
    return db_user_course