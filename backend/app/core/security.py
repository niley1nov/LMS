# backend/app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional

import jwt
# from passlib.context import CryptContext

from app.core.config import settings

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.JWT_ALGORITHM
JWT_SECRET_KEY = settings.JWT_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, 'ACCESS_TOKEN_EXPIRE_MINUTES', 60 * 24 * 7) # Default to 7 days

# --- Cookie Settings (Centralized) ---

# Since your Uvicorn is running with SSL (--ssl-certfile, --ssl-keyfile),
# your backend is on HTTPS. Assume frontend is also on HTTPS for dev (e.g., https://localhost:3000).
COOKIE_SECURE = True  # Always True if using HTTPS for backend and frontend

COOKIE_HTTPONLY = True

# For cross-origin requests (localhost:3000 to localhost:8000),
# SameSite=None is required for cookies to be sent with `withCredentials: true`.
# If SameSite=None, Secure attribute MUST be True.
COOKIE_SAMESITE = "None" # Explicitly set to "None"

COOKIE_MAX_AGE = ACCESS_TOKEN_EXPIRE_MINUTES * 60 # In seconds
COOKIE_PATH = "/"
COOKIE_DOMAIN = None # For localhost, None is correct. For production, set your domain if needed.


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Generates a JWT access token.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """
    Verifies a JWT token.
    Returns the decoded token payload if valid, otherwise None.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("DEBUG: Token verification failed - ExpiredSignatureError")
        return None
    except jwt.InvalidTokenError as e: # Catches InvalidSignatureError and other decode errors
        print(f"DEBUG: Token verification failed - InvalidTokenError: {e}")
        return None
    except Exception as e:
        print(f"DEBUG: Unexpected error during token verification: {e}")
        return None