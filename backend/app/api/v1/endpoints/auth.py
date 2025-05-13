# backend/app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response as FastAPIResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schemas import UserOut
from app.schemas.token_schemas import GoogleIdToken
from app.services.auth_service import auth_service
from app.db.session import get_db_session
from app.core import security

router = APIRouter()

@router.post("/google", response_model=UserOut)
async def login_with_google(
    response: FastAPIResponse,
    payload: GoogleIdToken,
    db: AsyncSession = Depends(get_db_session)
):
    print(f"DEBUG: POST /api/v1/auth/google endpoint hit with payload: {payload.model_dump_json()}")
    try:
        user, access_token = await auth_service.authenticate_with_google(
            db, google_id_token=payload.token
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
        print(f"DEBUG: HTTPException in login_with_google: {e.detail}")
        raise e
    except Exception as e:
        print(f"DEBUG: Unexpected error in login_with_google: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during authentication."
        )

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
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