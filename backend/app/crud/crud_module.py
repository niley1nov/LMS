# backend/app/crud/crud_module.py
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.crud.base_crud import CRUDBase
from sqlalchemy.orm import selectinload
from app.models.module_model import Module
from app.schemas.module_schemas import ModuleCreate, ModuleUpdate
import uuid

class CRUDModule(CRUDBase[Module, ModuleCreate, ModuleUpdate]):
    async def create_for_course(self, db: AsyncSession, course_id: uuid.UUID, obj_in: ModuleCreate):
        db_obj = Module(**obj_in.model_dump(), course_id=course_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_course(self, db: AsyncSession, course_id: uuid.UUID) -> List[Module]:
        stmt = select(self.model).where(self.model.course_id == course_id).order_by(self.model.order)
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def get_with_units(self, db: AsyncSession, module_id: int) -> Module | None:
        """
        Fetch the module *and* all its units in one go,
        so the .units attribute is pre‐loaded.
        """
        stmt = (
            select(self.model)
            .options(selectinload(self.model.units))
            .filter(self.model.id == module_id)
        )
        res = await db.execute(stmt)
        return res.scalars().first()

crud_module = CRUDModule(Module)
