# File: backend/app/routes/courses.py
from fastapi import APIRouter, Depends, HTTPException, status # Query removed if target_user_id is removed
from sqlalchemy.orm import Session, joinedload, selectinload
import uuid
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
    course_id: uuid.UUID, # <<<--- CORRECTED TYPE HINT TO uuid.UUID
    db: Session = Depends(get_db),
    current_user_payload: dict = Depends(get_current_user)
):
    """
    Fetch a single course by its ID, including its associated users,
    modules (ordered by 'order'), and units (ordered by 'order') within each module.
    """
    print(f"--- Fetching course with UUID: {course_id} (type: {type(course_id)}) ---") # Log input

    # This query now correctly compares a UUID column with a UUID path parameter
    course = db.query(models.Course)\
        .options(
            selectinload(models.Course.user_associations).joinedload(models.UserCourse.user),
            selectinload(models.Course.modules).selectinload(models.Module.units)
        )\
        .filter(models.Course.id == course_id)\
        .first()

    print(f"--- SQLAlchemy course object fetched: {course} ---") # Log the raw ORM object

    if not course:
        print(f"--- Course with UUID {course_id} not found in database. ---")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    # --- Logging related objects before Pydantic conversion ---
    if course:
        print(f"Course ID: {course.id} (type: {type(course.id)})")
        print(f"Course Name: {course.name}")
        print(f"Course Description: {course.description}")

        print("--- User Associations ---")
        if course.user_associations:
            for i, assoc in enumerate(course.user_associations):
                print(f"  Assoc {i+1}: User ID: {assoc.user_id}, Role: {assoc.role}, User Name: {assoc.user.name if assoc.user else 'N/A'}")
        else:
            print("  No user associations found.")

        print("--- Modules ---")
        if course.modules:
            for i, module in enumerate(course.modules):
                print(f"  Module {i+1}: ID: {module.id}, Title: {module.title}, Order: {module.order}")
                print("    --- Units ---")
                if module.units:
                    for j, unit in enumerate(module.units):
                        # Accessing unit_type which maps to 'type' in DB
                        print(f"      Unit {j+1}: ID: {unit.id}, Title: {unit.title}, Type: {unit.unit_type}, Order: {unit.order}")
                else:
                    print("      No units found for this module.")
        else:
            print("  No modules found for this course.")
    
    # Optional: Authorization check (ensure user_id_from_token is handled correctly)
    user_id_from_token_str = current_user_payload.get("sub")
    if not user_id_from_token_str:
        # This should ideally be caught by get_current_user if token is invalid
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: User subject missing.")
    try:
        user_id_from_token = int(user_id_from_token_str)
        is_enrolled = any(assoc.user_id == user_id_from_token for assoc in course.user_associations)
        if not is_enrolled:
            # Add more sophisticated role-based access if needed (e.g., admin/teacher override)
            # print(f"--- Authorization Failed: User {user_id_from_token} not enrolled in course {course_id} ---")
            # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this course.")
            pass # Temporarily bypassing auth check for debugging Pydantic issue
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format in token.")
    except AttributeError: # In case course.user_associations is None (should not happen with selectinload)
        print("--- Error accessing user_associations, it might be None ---")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error processing course data.")


    print("--- Attempting to return course object for Pydantic serialization ---")
    return course

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

@router.post("", response_model=schemas.CourseOut, status_code=status.HTTP_201_CREATED)
def create_course(
    course_in: schemas.CourseCreate,
    db: Session = Depends(get_db),
    current_user_payload: dict = Depends(get_current_user) # JWT payload
):
    """
    Create a new course. The creator is automatically enrolled as a teacher.
    """
    creator_id_str = current_user_payload.get("sub")
    if not creator_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not identify user from token."
        )
    
    try:
        creator_id = int(creator_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format in token."
        )

    # Check if user exists (optional, but good practice if sub claim could be stale)
    creator = db.query(models.User).filter(models.User.id == creator_id).first()
    if not creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Creator user with ID {creator_id} not found."
        )

    # Create the new course
    db_course = models.Course(name=course_in.name, description=course_in.description)
    db.add(db_course)
    
    try:
        db.flush() # Flush to get the db_course.id before creating the association

        # Associate the creator with the course as a teacher
        user_course_association = models.UserCourse(
            user_id=creator_id,
            course_id=db_course.id,
            role=schemas.Role.TEACHER # Use the Role enum from your schemas
        )
        db.add(user_course_association)
        
        db.commit()
        db.refresh(db_course) # Refresh to load relationships like user_associations
        
        # Manually construct the CourseOut to include the creator in the 'users' list
        # This is because db_course.user_associations might not be immediately populated
        # in the way CourseOut expects without another query or careful session management.
        # For simplicity, we'll build it based on what we know.
        
        # Re-fetch the course with its associations to ensure the response is complete
        # This is the most reliable way to populate CourseOut correctly after creation.
        populated_course = db.query(models.Course)\
            .options(selectinload(models.Course.user_associations).joinedload(models.UserCourse.user))\
            .filter(models.Course.id == db_course.id)\
            .first()

        if not populated_course: # Should not happen if commit was successful
             raise HTTPException(status_code=500, detail="Failed to retrieve course after creation.")

        users_for_response = []
        for assoc in populated_course.user_associations:
            users_for_response.append(schemas.UserForCourseResponse(
                id=assoc.user.id,
                email=assoc.user.email,
                name=assoc.user.name,
                role=assoc.role.value
            ))

        return schemas.CourseOut(
            id=populated_course.id,
            name=populated_course.name,
            description=populated_course.description,
            users=users_for_response
        )

    except Exception as e:
        db.rollback()
        # Log the error e for server-side debugging
        # print(f"Error creating course: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the course."
        )