# backend/app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response as FastAPIResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schemas import UserOut
from app.schemas.token_schemas import GoogleIdToken # <--- IMPORT THE CORRECT SCHEMA
from app.services.auth_service import auth_service
from app.db.session import get_db_session
from app.api import deps
from app.core import security
from app.models.user import User as UserModel

router = APIRouter()

# The class GoogleTokenInput(Token) is no longer needed here
# if GoogleIdToken schema is defined in token_schemas.py

@router.post("/auth/google", response_model=UserOut)
async def login_with_google(
    response: FastAPIResponse,
    payload: GoogleIdToken, # <--- USE THE CORRECT SCHEMA HERE
    db: AsyncSession = Depends(get_db_session)
):
    print(f"DEBUG: POST /api/v1/auth/google endpoint hit with payload: {payload.model_dump_json()}")
    try:
        # auth_service.authenticate_with_google expects the raw google_id_token string
        user, access_token = await auth_service.authenticate_with_google(
            db, google_id_token=payload.token # Access the token string from the payload
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=security.COOKIE_HTTPONLY,
            secure=security.COOKIE_SECURE,
            samesite=security.COOKIE_SAMESITE,
            max_age=security.COOKIE_MAX_AGE,
            path=security.COOKIE_PATH,
            # domain=security.COOKIE_DOMAIN,
        )
        return user
    except HTTPException as e:
        # print(f"DEBUG: HTTPException in login_with_google: {e.detail}")
        raise e
    except Exception as e:
        # print(f"DEBUG: Unexpected error in login_with_google: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during authentication."
        )

@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: FastAPIResponse):
    print("DEBUG: POST /api/v1/auth/logout endpoint hit!")
    response.delete_cookie(
        key="access_token",
        path=security.COOKIE_PATH,
        httponly=security.COOKIE_HTTPONLY,
        secure=security.COOKIE_SECURE,
        samesite=security.COOKIE_SAMESITE,
        # domain=security.COOKIE_DOMAIN,
    )
    return

@router.get("/users/me", response_model=UserOut)
async def read_users_me(
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    print(f"DEBUG: GET /api/v1/users/me endpoint hit by user: {current_user.email if current_user else 'None'}")
    return current_user
