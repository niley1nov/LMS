# backend/app/api/v1/api_v1.py
from fastapi import APIRouter
from .endpoints import auth, courses, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])