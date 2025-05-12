# backend/app/services/auth_service.py
from typing import Tuple, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import traceback # For detailed error logging

from app.core.config import settings
from app.core import security
from app.crud.crud_user import crud_user
from app.models.user import User as UserModel

class AuthService:
    async def verify_google_token(self, token: str) -> dict:
        """
        Verifies the Google ID token and returns the idinfo.
        Raises HTTPException if the token is invalid.
        """
        print(f"DEBUG: Verifying Google token. Client ID used for verification: {settings.GOOGLE_CLIENT_ID}")
        if not settings.GOOGLE_CLIENT_ID:
            print("ERROR: GOOGLE_CLIENT_ID is not set in backend settings!")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Google Client ID not configured on server."
            )
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID  # This audience MUST match the token's 'aud' claim
            )
            print(f"DEBUG: Google token verified successfully. idinfo: {idinfo}")
            # You might want to check idinfo['iss'] to verify the issuer
            if idinfo.get('iss') not in ['accounts.google.com', 'https://accounts.google.com']:
                print(f"ERROR: Invalid token issuer: {idinfo.get('iss')}")
                raise ValueError('Wrong issuer.')
            return idinfo
        except ValueError as e:
            print(f"ERROR: Google token verification failed. ValueError: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Google token: {e}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e: # Catch any other unexpected errors during verification
            print(f"ERROR: Unexpected error during Google token verification: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error verifying Google token."
            )

    async def authenticate_with_google(
        self, db: AsyncSession, *, google_id_token: str
    ) -> Tuple[UserModel, str]:
        """
        Authenticates a user with a Google ID token.
        Upserts the user in the database and generates an access token.
        """
        print(f"DEBUG: Authenticating with Google token: {google_id_token[:30]}...") # Log part of token
        
        idinfo = await self.verify_google_token(google_id_token)
        print(f"DEBUG: idinfo received: {idinfo}")

        google_sub = idinfo.get('sub')
        email = idinfo.get('email')
        name = idinfo.get('name') # This can be None

        if not google_sub or not email:
            print(f"ERROR: Google token missing 'sub' or 'email'. sub: {google_sub}, email: {email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Google token missing required 'sub' or 'email' fields."
            )
        
        print(f"DEBUG: Attempting to upsert user. google_sub: {google_sub}, email: {email}, name: {name}")
        try:
            user = await crud_user.upsert_google_user(
                db, google_sub=google_sub, email=email, name=name
            )
            print(f"DEBUG: User upserted/retrieved: ID {user.id if user else 'None'}, Email {user.email if user else 'None'}")
        except Exception as e:
            print(f"ERROR: Database error during upsert_google_user: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error processing user information."
            )

        if not user:
            print("ERROR: crud_user.upsert_google_user returned None unexpectedly.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not create or update user information."
            )

        print(f"DEBUG: Generating access token for user ID: {user.id}")
        try:
            access_token = security.create_access_token(subject=str(user.id))
            print(f"DEBUG: Access token generated: {access_token[:30]}...")
        except Exception as e:
            print(f"ERROR: Error generating access token: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error generating access token."
            )
            
        return user, access_token

auth_service = AuthService()