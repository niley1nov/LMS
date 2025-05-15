# backend/app/api/v1/api_v1.py
from fastapi import APIRouter
from .endpoints import auth, courses, users, modules, units

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(modules.router, prefix="/courses/{course_id}/modules", tags=["Modules"])
api_router.include_router(units.router, prefix="/modules/{module_id}/units", tags=["Units"])