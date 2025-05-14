# backend/app/services/course_service.py
from typing import List, Optional
import uuid
import traceback

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.crud.crud_course import crud_course
from app.crud.crud_user import crud_user
from app.models.course import Course as CourseModel
from app.models.user_course import UserCourse as UserCourseModel
from app.schemas.course_schemas import CourseCreate
from app.schemas.user_course_schemas import UserCourseCreate, UserCourseRole
from app.models.user import User as UserModel
from app.models.enums import UserRoleEnum # Assuming you might have a global admin role defined here or in UserModel

class CourseService:
    async def get_courses_for_user(
        self, db: AsyncSession, *, user: UserModel, skip: int = 0, limit: int = 100
    ) -> List[CourseModel]:
        print(f"DEBUG: CourseService.get_courses_for_user called for user ID: {user.id}")
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        try:
            courses = await crud_course.get_multi_for_user(db, user_id=user.id, skip=skip, limit=limit)
            print(f"DEBUG: crud_course.get_multi_for_user returned {len(courses)} courses.")
            return courses
        except Exception as e:
            print(f"ERROR in CourseService.get_courses_for_user: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching courses.")

    async def get_course_by_id_for_user(
        self, db: AsyncSession, *, course_id: uuid.UUID, user: UserModel
    ) -> Optional[CourseModel]:
        """
        Service to get a specific course by ID.
        Authorization:
        - User must be enrolled in the course.
        - OR User must be a global admin (example, if you have such a role).
        - OR User must be a teacher of this specific course (already covered by enrollment).
        """
        print(f"DEBUG: CourseService.get_course_by_id_for_user called for course_id: {course_id}, requested by user_id: {user.id}")
        try:
            course = await crud_course.get_with_details(db, course_uuid=course_id)
            if not course:
                # Return 404 if course doesn't exist at all
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

            # --- Authorization Check ---
            is_enrolled = False
            user_role_in_course: Optional[UserCourseRole] = None

            for assoc in course.user_associations:
                if assoc.user_id == user.id:
                    is_enrolled = True
                    user_role_in_course = assoc.role # Get the user's specific role in this course
                    break
            
            # Example: Check for a global admin role (if your UserModel has such a field)
            # is_global_admin = hasattr(user, 'global_role') and user.global_role == UserRoleEnum.admin
            # Or, if you have an is_superuser flag:
            is_global_admin = hasattr(user, 'is_superuser') and user.is_superuser

            print(f"DEBUG AuthZ: User {user.id} - Enrolled: {is_enrolled}, Role in Course: {user_role_in_course}, Global Admin: {is_global_admin if hasattr(user, 'is_superuser') else 'N/A'}")

            # Allow access if user is enrolled OR is a global admin
            if not is_enrolled and not is_global_admin:
                # If not enrolled and not an admin, deny access.
                # Raising 403 Forbidden is more appropriate than 404 if the course exists but user lacks permission.
                # However, some prefer 404 to not reveal existence of the resource.
                print(f"DEBUG AuthZ: User {user.id} is NOT ENROLLED and NOT ADMIN for course {course_id}. Access denied.")
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this course.")
            
            # If execution reaches here, the user is authorized
            print(f"DEBUG AuthZ: User {user.id} authorized for course {course_id}.")
            print(f"DEBUG: Course {course_id} retrieved successfully for user {user.id}.")
            return course
        except HTTPException:
            raise # Re-raise HTTPExceptions (like 404 or 403 from above)
        except Exception as e:
            print(f"ERROR in CourseService.get_course_by_id_for_user: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching course details.")


    async def enroll_new_user_in_course(
        self, db: AsyncSession, *, enrollment_data: UserCourseCreate, current_user: UserModel
    ) -> UserCourseModel:
        print(f"DEBUG: CourseService.enroll_new_user_in_course called by user {current_user.id} for user {enrollment_data.user_id} in course {enrollment_data.course_id}")
        try:
            # Authorization: e.g., only admin or teacher of the course can enroll others.
            # For self-enrollment, enrollment_data.user_id would == current_user.id
            # This logic needs to be implemented based on your requirements.
            # For now, let's assume an admin can enroll anyone, or user can enroll self.
            # is_global_admin = hasattr(current_user, 'is_superuser') and current_user.is_superuser
            # if enrollment_data.user_id != current_user.id and not is_global_admin:
            #     # Further check if current_user is a teacher of enrollment_data.course_id
            #     # This would require fetching the course and checking current_user's role in it.
            #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to enroll this user.")


            target_user = await crud_user.get(db, record_id=enrollment_data.user_id)
            if not target_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {enrollment_data.user_id} not found")

            target_course = await crud_course.get(db, record_id=enrollment_data.course_id)
            if not target_course:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {enrollment_data.course_id} not found")

            result = await crud_course.enroll_user(
                db,
                user_id=enrollment_data.user_id,
                course_id=enrollment_data.course_id,
                role=enrollment_data.role
            )

            if isinstance(result, str):
                if result == "already_exists":
                    existing_stmt = select(UserCourseModel).filter_by(user_id=enrollment_data.user_id, course_id=enrollment_data.course_id)
                    existing_assoc_result = await db.execute(existing_stmt)
                    existing_assoc = existing_assoc_result.scalars().first()
                    current_role_value = existing_assoc.role.value if existing_assoc else "unknown"
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"User {enrollment_data.user_id} is already associated with course {enrollment_data.course_id}. Current role: {current_role_value}."
                    )
                elif result == "user_not_found":
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {enrollment_data.user_id} not found for enrollment.")
                elif result == "course_not_found":
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with id {enrollment_data.course_id} not found for enrollment.")

            if not isinstance(result, UserCourseModel):
                print(f"ERROR: crud_course.enroll_user returned unexpected value: {result}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to enroll user due to an unexpected issue.")
            
            print(f"DEBUG: User {enrollment_data.user_id} enrolled in course {enrollment_data.course_id} successfully.")
            return result
        except HTTPException:
            raise
        except Exception as e:
            print(f"ERROR in CourseService.enroll_new_user_in_course: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error enrolling user.")

    async def create_new_course(
        self, db: AsyncSession, *, course_data: CourseCreate, creator: UserModel
    ) -> CourseModel:
        print(f"DEBUG: CourseService.create_new_course called by creator ID: {creator.id}")
        if not creator:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not identify course creator.")
        try:
            new_course = await crud_course.create_course_with_creator_enrollment(
                db, obj_in=course_data, creator_id=creator.id, creator_role=UserCourseRole.teacher
            )
            if not new_course:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create course.")
            print(f"DEBUG: New course created with ID: {new_course.id}")
            return new_course
        except Exception as e:
            print(f"ERROR in CourseService.create_new_course: {e}")
            traceback.print_exc()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating new course.")

course_service = CourseService()
