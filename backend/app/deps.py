from fastapi import HTTPException, Depends, Cookie, status
# Make sure to import jwt from the PyJWT library
import jwt
from jwt import PyJWTError, ExpiredSignatureError, InvalidSignatureError # Specific errors from PyJWT
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from .config import JWT_SECRET, JWT_ALGORITHM
from .database import SessionLocal # Assuming SessionLocal is defined in database.py

# Standard dependency to get a database session
def get_db():
    """
    Dependency that provides a SQLAlchemy database session.
    Ensures the session is closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    # FastAPI will automatically look for a cookie named "access_token"
    # If not found, access_token will be None.
    access_token: Optional[str] = Cookie(None, alias="access_token") # Explicitly set alias if needed, though FastAPI often infers it
) -> Dict[str, Any]: # Explicitly type hint the return as a dictionary
    """
    Dependency to get the current user from the JWT access token
    stored in an HTTP-only cookie.

    Raises:
        HTTPException: 401 if token is missing, invalid, or expired,
                       or if essential claims are missing.
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Token missing from cookies.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Decode the JWT using PyJWT.
        # This function verifies the signature and can also check expiration
        # if 'exp' claim is present and validated by the library.
        payload = jwt.decode(
            access_token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM]
            # PyJWT verifies 'exp' by default if present.
            # You can pass options={"verify_exp": True} if you want to be explicit or handle leeway.
        )
        
        # Validate essential claims (e.g., 'sub' for user ID)
        user_id_from_token: Optional[str] = payload.get("sub") # 'sub' is standard for subject (user ID)
        if user_id_from_token is None:
            # This means the token is validly signed but doesn't contain the user identifier
            # which is a critical piece of information for your application.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: User identifier (sub) missing.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Optional: You could add more checks here, e.g., if the user still exists in DB,
        # or if their account is active. However, this adds a DB lookup to every
        # authenticated request. For pure JWT statelessness, relying on the token's
        # validity and essential claims is often the first step.

        return payload # Return the decoded payload dictionary

    except ExpiredSignatureError:
        # Specific error for expired tokens from PyJWT
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidSignatureError:
        # Specific error for signature mismatch from PyJWT
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PyJWTError as e: # Catch-all for other PyJWT errors
        # This could be due to a malformed token, wrong algorithm, etc.
        # You might want to log the error 'e' for server-side debugging.
        # print(f"PyJWTError: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials: Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )