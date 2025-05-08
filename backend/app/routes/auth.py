# File: backend/app/routes/auth.py (update upsert_user)
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import Response
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from ..deps import get_current_user
import jwt
from ..schemas import UserOut, UserBase
from ..config import GOOGLE_CLIENT_ID, JWT_SECRET, JWT_ALGORITHM, env
from ..database import SessionLocal
from ..models import User

router = APIRouter()

class GoogleToken(BaseModel):
    token: str

@router.post("/auth/google", response_model=UserOut)
async def google_auth(payload: GoogleToken, response: Response):
    try:
        idinfo = id_token.verify_oauth2_token(
            payload.token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    google_sub = idinfo['sub']
    email = idinfo.get('email')
    name = idinfo.get('name', '')

    # Upsert user in DB and get internal user_id
    db = SessionLocal()
    user = db.query(User).filter(User.google_sub == google_sub).first()
    if user:
        user.email = email
        user.name = name
    else:
        user = User(google_sub=google_sub, email=email, name=name)
        db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    
    user_id = user.id
    
    # Issue JWT
    token = jwt.encode({'sub': str(user_id), 'email': email, 'name': name}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # Choose cookie policy based on environment

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=3600,  # 1 hour
        path="/"
    )
    return user

@router.post("/auth/logout")
def logout():
    # Create a response with 204 status
    resp = Response(status_code=status.HTTP_204_NO_CONTENT)
    # Delete the cookie on that response
    resp.delete_cookie(
        key="access_token",
        path="/",                    # must match how you set it
        httponly=True,
        secure=True,
        samesite="none",             # same as when you set it
    )
    return resp

@router.get("/me", response_model=UserBase) # Changed response_model to UserBase
def read_current_user(user: dict = Depends(get_current_user)):
    return UserBase(
        id=int(user.get("sub")),
        email=user.get("email"),
        name=user.get("name")
    )
