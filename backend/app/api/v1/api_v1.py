# backend/app/api/v1/api_v1.py
from fastapi import APIRouter
from .endpoints import auth, courses, users # Import your new auth router
# ... import other endpoint routers ...

api_router = APIRouter()
api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(courses.router, prefix="/courses", tags=["Courses"]) # Add this line
api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
# ... include other routers ...