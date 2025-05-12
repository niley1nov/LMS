# backend/app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.session import get_db_session
from app.models.user import User as UserModel
from app.schemas.user_schemas import UserOut, UserUpdate # Use appropriate Pydantic schemas
from app.api import deps # Your API dependencies
from app.services.user_service import user_service # User service layer
# from app.models.enums import UserRoleEnum # If using for role checks

router = APIRouter()

# GET /users/me is already in auth.py and returns the current authenticated user.
# If you want a more detailed profile for /me that might differ from a generic UserOut,
# you could create a specific schema for it.

@router.get("/{user_id}", response_model=UserOut, summary="Get user by ID")
async def read_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(deps.get_current_active_user) # Ensures requester is authenticated
):
    """
    Retrieve a specific user by their ID.
    Authorization rules (e.g., admin access or self-access) are handled by the service layer.
    """
    try:
        user = await user_service.get_user_by_id(db, user_id=user_id, current_user=current_user)
        if not user: # Should be handled by service raising HTTPException, but as a safeguard
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        # Log e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving user.")


@router.put("/{user_id}", response_model=UserOut, summary="Update user profile")
async def update_user_profile_endpoint(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Update a user's profile information.
    A user can update their own profile. Admins might be able to update others (logic in service).
    """
    user_to_update = await user_service.get_user_by_id(db, user_id=user_id, current_user=current_user) # Fetch first to ensure it exists
    if not user_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found to update")

    try:
        updated_user = await user_service.update_user_profile(
            db, user_to_update=user_to_update, user_data=user_in, current_user=current_user
        )
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        # Log e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating user profile.")


@router.get("", response_model=List[UserOut], summary="List all users (Admin Only - Placeholder)")
# @router.get("/", response_model=List[UserOut], include_in_schema=False) # Alias
async def list_all_users(
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(deps.get_current_active_user), # For authorization
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve a list of all users.
    **Note: This endpoint should be strictly protected and accessible only by administrators.**
    The authorization logic is currently a placeholder in the service.
    """
    # Placeholder for Admin Authorization - implement this robustly in the service or a dependency!
    # For example, using a role check:
    # if not current_user.role == UserRoleEnum.admin: # Assuming a global 'role' on UserModel
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to list all users")
    # print(f"Warning: Listing all users endpoint accessed by {current_user.email}. Ensure proper admin protection.")

    try:
        users = await user_service.get_all_users(db, current_user=current_user, skip=skip, limit=limit)
        return users
    except HTTPException:
        raise
    except Exception as e:
        # Log e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error retrieving users.")


@router.delete("/{user_id}", response_model=UserOut, summary="Delete a user (Admin Only - Placeholder)")
async def delete_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Delete a user by their ID.
    **Note: This endpoint should be strictly protected and accessible only by administrators.**
    """
    # Placeholder for Admin Authorization
    # if not current_user.role == UserRoleEnum.admin:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete users")
    # print(f"Warning: Delete user endpoint accessed by {current_user.email} for user_id {user_id}. Ensure proper admin protection.")

    try:
        deleted_user = await user_service.delete_user_by_id(db, user_id_to_delete=user_id, current_user=current_user)
        if not deleted_user: # Should be handled by service raising HTTPException
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found for deletion.")
        return deleted_user # Or return a confirmation message
    except HTTPException:
        raise
    except Exception as e:
        # Log e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting user.")

