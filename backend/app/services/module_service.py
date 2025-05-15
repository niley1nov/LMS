# backend/app/services/module_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_module import crud_module
from app.models.user import User
from app.schemas.module_schemas import ModuleCreate
import uuid

class ModuleService:
    async def create_module(self, db: AsyncSession, course_id: uuid.UUID, module_data: ModuleCreate, creator: User):
        # 1) create the row
        module = await crud_module.create_for_course(
            db, course_id=course_id, obj_in=module_data
        )

        # 2) re-fetch it with units eagerly loaded
        full_module = await crud_module.get_with_units(db, module_id=module.id)
        return full_module

    async def get_modules_for_course(self, db: AsyncSession, course_id: uuid.UUID, user: User):
        # TODO: optional auth checks
        return await crud_module.get_multi_by_course(db, course_id=course_id)

module_service = ModuleService()
