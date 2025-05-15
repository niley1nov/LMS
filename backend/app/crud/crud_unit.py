# backend/app/crud/crud_unit.py
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.crud.base_crud import CRUDBase
from app.models.unit import Unit
from app.schemas.unit_schemas import UnitCreate, UnitUpdate

class CRUDUnit(CRUDBase[Unit, UnitCreate, UnitUpdate]):
    async def create_for_module(self, db: AsyncSession, module_id: int, obj_in: UnitCreate):
        payload = obj_in.model_dump(mode="json")
        payload["unit_type"] = obj_in.unit_type.name
        db_obj = Unit(**payload, module_id=module_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_module(self, db: AsyncSession, module_id: int) -> List[Unit]:
        stmt = select(self.model).where(self.model.module_id == module_id).order_by(self.model.order)
        result = await db.execute(stmt)
        return result.scalars().all()

crud_unit = CRUDUnit(Unit)
