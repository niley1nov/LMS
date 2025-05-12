# backend/app/schemas/token_schemas.py
from pydantic import BaseModel
from typing import Optional
import uuid # Keep if other schemas here use it

class Token(BaseModel):
    """
    Schema for your application's JWT access token (when you send it to the client).
    """
    access_token: str
    token_type: str = "bearer" # Default token type
    # refresh_token: Optional[str] = None # If using refresh tokens

class TokenPayload(BaseModel):
    """
    Schema for the payload within your application's JWT.
    """
    sub: Optional[str] = None # Subject (user identifier, e.g., user ID)
    # You can add other claims you put in your JWT payload, like email, name, roles etc.
    # user_id: Optional[int] = None # Redundant if 'sub' is user_id
    # exp: Optional[int] = None # Expiration time (handled by JWT library during creation/validation)
    # iat: Optional[int] = None # Issued at time (handled by JWT library)
    # jti: Optional[str] = None # JWT ID (handled by JWT library)

class GoogleIdToken(BaseModel):
    """
    Schema for receiving the Google ID Token from the frontend.
    """
    token: str # This field name matches what the frontend sends: {"token": "..."}
