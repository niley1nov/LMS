# backend/app/api/deps.py
from typing import Optional, AsyncGenerator

from fastapi import Depends, HTTPException, status, Request # Request is needed to access cookies
from sqlalchemy.ext.asyncio import AsyncSession
import jwt # Still used by security.verify_token internally, but not directly here for decoding
import asyncio
import traceback

from app.core.config import settings # Your Pydantic settings
from app.core import security      # Your security utilities (verify_token)
from app.db.session import get_db_session # Your ASYNC database session dependency
from app.models.user import User as UserModel # Your SQLAlchemy User model
from app.crud.crud_user import crud_user            # Your CRUD operations for user
from app.schemas.token_schemas import TokenPayload # Your Pydantic schema for token payload

async def get_current_user_from_cookie(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
) -> Optional[UserModel]:
    """
    Dependency to get the current user from the access_token cookie.
    Verifies the token, and fetches the user from the database.
    Returns the SQLAlchemy UserModel instance or None if not authenticated or user not found.
    """
    print('--- get_current_user_from_cookie ---')
    access_token: Optional[str] = request.cookies.get("access_token")
    print(f'access_token: {access_token[:30] if access_token else "None"}...')

    if not access_token:
        return None

    try:
        payload_dict = security.verify_token(access_token)
        print(f'payload_dict from token: {payload_dict}')
        if payload_dict is None:
            return None

        try:
            token_data = TokenPayload(**payload_dict)
            print(f'token_data (Pydantic): {token_data}')
        except Exception as e_pydantic: # Catches Pydantic validation errors
            print(f"ERROR: Token payload validation error: {e_pydantic}")
            traceback.print_exc() # Log Pydantic validation errors
            return None

        if token_data.sub is None:
            print("ERROR: token_data.sub is None")
            return None

        try:
            user_id = int(token_data.sub)
            print(f'user_id from token: {user_id}')
        except ValueError:
            print(f"ERROR: Cannot convert token_data.sub ('{token_data.sub}') to int")
            return None

        print(f"DEBUG: Type of crud_user in deps: {type(crud_user)}")
        print(f"DEBUG: crud_user object ID in deps: {id(crud_user)}")
        print(f"DEBUG: crud_user has 'get' attribute: {hasattr(crud_user, 'get')}")
        if hasattr(crud_user, 'get'):
            get_method = crud_user.get
            print(f"DEBUG: crud_user.get method object: {get_method}")
            print(f"DEBUG: crud_user.get is callable: {callable(get_method)}")
            if hasattr(get_method, '__func__'):
                print(f"DEBUG: Is crud_user.get an async function? {asyncio.iscoroutinefunction(get_method.__func__)}")
            else:
                print(f"DEBUG: Is crud_user.get an async function? {asyncio.iscoroutinefunction(get_method)}")

        print(f"DEBUG: Attempting to call await crud_user.get(db, id={user_id})")
        user: Optional[UserModel] = None
        try:
            user = await crud_user.get(db=db, record_id=user_id)
        except Exception as e_crud_get:
            print(f"ERROR: Exception during crud_user.get call: {e_crud_get}")
            traceback.print_exc()
            return None

        print(f'user from crud_user.get: {user.id if user else "None"}')
        
        if not user:
            return None

        return user

    except jwt.ExpiredSignatureError:
        print("DEBUG: Token verification failed - ExpiredSignatureError")
        # traceback.print_exc() # Optional: if you want full trace for expired tokens too
        return None
    except jwt.PyJWTError as e_jwt: # Catch other JWT errors
        print(f"DEBUG: Token verification failed - PyJWTError: {e_jwt}")
        traceback.print_exc() # Log PyJWT errors
        return None
    except Exception as e_outer: # Catch any other unexpected errors during the process
        print(f"CRITICAL ERROR: Unexpected error in get_current_user_from_cookie: {e_outer}")
        traceback.print_exc() # <--- ADDED TRACEBACK HERE
        return None


async def get_current_active_user(
    current_user: Optional[UserModel] = Depends(get_current_user_from_cookie)
) -> UserModel:
    """
    Dependency to get the current authenticated user.
    If the user is not found (i.e., current_user is None), it raises an HTTPException.
    You can add checks for user.is_active here if your UserModel has such a field.
    """
    print('get_current_active_user')
    print(current_user)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated or user not found.",
            headers={"WWW-Authenticate": "Bearer"}, # Standard header for 401
        )
    # Example: Check if the user is active (requires an 'is_active' boolean field in your UserModel)
    # if hasattr(current_user, 'is_active') and not current_user.is_active:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return current_user


async def get_optional_current_user(
    current_user: Optional[UserModel] = Depends(get_current_user_from_cookie)
) -> Optional[UserModel]:
    """
    Dependency to optionally get the current user.
    If the token is missing or invalid, or user not found, it returns None.
    Does not raise an HTTPException, allowing routes to behave differently
    for authenticated vs. unauthenticated users.
    """
    return current_user

# Example: Dependency for requiring a specific role (if you implement roles)
# from app.models.enums import UserRoleEnum
# def require_role(required_role: UserRoleEnum):
#     async def role_checker(current_user: UserModel = Depends(get_current_active_user)) -> UserModel:
#         if not hasattr(current_user, 'role') or current_user.role != required_role:
#             # Assuming your UserModel has a 'role' attribute that matches UserRoleEnum
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail=f"User does not have the required role: {required_role.value}"
#             )
#         return current_user
#     return role_checker

# Example usage for role requirement:
# @router.post("/admin/create-thing", dependencies=[Depends(require_role(UserRoleEnum.admin))])
# async def create_admin_thing(...):
#     ...
