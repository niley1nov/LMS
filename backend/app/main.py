import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import jwt

# Load environment (.env.development or .env.production)
env = os.getenv("ENV", "development")
load_dotenv(f".env.{env}", override=True)

# Config variables
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")  # Override in prod .env
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# CORS origins
target_frontend = os.getenv("FRONTEND_URL", "http://localhost:3000")
origins = [target_frontend] if env != "development" else ["http://localhost:3000"]

# FastAPI setup
app = FastAPI()
def get_origins():
    env = os.getenv("ENV", "development")
    dev_origins = ["http://localhost:3000"]
    prod_frontend = os.getenv("FRONTEND_URL")
    prod_origins = [prod_frontend] if prod_frontend else []
    return dev_origins + prod_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_origins(),      # explicitly allow local & production front end
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for Google ID token payload
class GoogleToken(BaseModel):
    token: str

# Stub for upserting or fetching user from DB
def upsert_user(google_sub: str, email: str, name: str) -> str:
    # TODO: Implement real DB logic here
    return google_sub

@app.get("/")
def read_root():
    return {"message": "LMS Backend working"}

@app.post("/auth/google")
async def google_auth(payload: GoogleToken, response: Response):
    # Verify the Google ID token
    try:
        idinfo = id_token.verify_oauth2_token(
            payload.token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    # Extract user info
    google_sub = idinfo["sub"]
    email = idinfo.get("email")
    name = idinfo.get("name", "")

    # Upsert user in DB
    user_id = upsert_user(google_sub, email, name)

    # Create a JWT containing user_id, email, and name
    app_token = jwt.encode(
        {"sub": user_id, "email": email, "name": name},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    # Set token in HttpOnly, Secure cookie
    response.set_cookie(
        key="access_token",
        value=app_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=3600  # 1 hour
    )

    return {"user": {"id": user_id, "email": email, "name": name}}

# Dependency to retrieve current user from cookie
async def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

@app.get("/protected")
def protected_route(user=Depends(get_current_user)):
    # Greet by name instead of email
    name = user.get("name") or user.get("email")
    return {"message": f"Hello {name}, you have access!"}
