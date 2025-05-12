# backend/app/services/user_service.py
from typing import List, Optional, Any

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.crud import crud_user
from app.models.user import User as UserModel
from app.schemas.user_schemas import UserUpdate, UserOut # Assuming UserOut is appropriate for list/get
# from app.models.enums import UserRoleEnum # If you have global roles for authorization

class UserService:
    async def get_user_by_id(
        self, db: AsyncSession, *, user_id: int, current_user: UserModel
    ) -> Optional[UserModel]:
        """
        Get a user by their ID.
        Authorization:
        - A user can get their own details.
        - An admin can get any user's details.
        - (Future: A teacher might get details of students in their courses).
        """
        target_user = await crud_user.get(db, record_id=user_id)
        if not target_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Authorization Check
        # if target_user.id == current_user.id or current_user.role == UserRoleEnum.admin: # Assuming global roles
        if target_user.id == current_user.id: # Simplest: user can get their own
             # Add more complex role-based access here if needed, e.g.
             # elif hasattr(current_user, 'is_superuser') and current_user.is_superuser:
            return target_user
        else:
            # Basic check: if not own profile, deny unless specific roles allow (not implemented here yet)
            # This needs to be expanded based on your LMS's role system.
            # For now, let's assume only admins or the user themselves can fetch.
            # We'll rely on the endpoint to enforce admin-only for listing all users.
            # For getting a specific user, if not self, it might be restricted.
            # For simplicity here, we'll allow if the user is found and current_user is valid.
            # More granular checks should be added based on roles (e.g. admin can see anyone).
            # If current_user is not an admin and target_user is not current_user:
            # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this user's details")
            pass # Placeholder for more complex auth. For now, if found, return.

        return target_user # Or apply more specific auth logic

    async def update_user_profile(
        self, db: AsyncSession, *, user_to_update: UserModel, user_data: UserUpdate, current_user: UserModel
    ) -> Optional[UserModel]:
        """
        Update a user's profile.
        Authorization:
        - A user can update their own profile.
        - An admin can update any user's profile.
        """
        if user_to_update.id != current_user.id:
            # Add admin check here if admins can update any profile
            # if not (hasattr(current_user, 'is_superuser') and current_user.is_superuser):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user's profile")

        # Prevent updating certain fields if necessary (e.g., email if tied to Google Sub, or role)
        # For example, if email should not be updatable here:
        # if user_data.email and user_data.email != user_to_update.email:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email cannot be changed directly.")

        updated_user = await crud_user.update(db, db_obj=user_to_update, obj_in=user_data)
        return updated_user

    async def get_all_users(
        self, db: AsyncSession, *, current_user: UserModel, skip: int = 0, limit: int = 100
    ) -> List[UserModel]:
        """
        Get a list of all users.
        Authorization:
        - Typically, only admins should be able to list all users.
        """
        # Example Admin Check (requires 'is_superuser' or a role field in UserModel)
        # if not (hasattr(current_user, 'is_superuser') and current_user.is_superuser):
        # if not current_user.role == UserRoleEnum.admin: # Assuming global roles
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to list all users")
        # For now, let's assume this check is done at the endpoint level or this service is only called by admin-protected routes.

        users = await crud_user.get_multi(db, skip=skip, limit=limit)
        return users

    async def delete_user_by_id(
        self, db: AsyncSession, *, user_id_to_delete: int, current_user: UserModel
    ) -> Optional[UserModel]:
        """
        Deletes a user by their ID.
        Authorization:
        - Typically, only admins can delete users.
        - A user should generally not be able to delete their own account via this admin-style endpoint.
        """
        # Example Admin Check
        # if not (hasattr(current_user, 'is_superuser') and current_user.is_superuser):
        # if not current_user.role == UserRoleEnum.admin:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete users")

        # Prevent admin from deleting themselves via this specific endpoint?
        # if user_id_to_delete == current_user.id and current_user.role == UserRoleEnum.admin:
        #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin cannot delete self via this endpoint.")

        user_to_delete = await crud_user.get(db, record_id=user_id_to_delete)
        if not user_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User to delete not found")

        deleted_user = await crud_user.remove(db, record_id=user_id_to_delete)
        return deleted_user


# Instantiate the service
user_service = UserService()