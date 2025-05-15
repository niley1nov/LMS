# backend/app/services/unit_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.crud_unit import crud_unit
from app.models.user import User
from app.schemas.unit_schemas import UnitCreate

class UnitService:
    async def create_unit(self, db: AsyncSession, module_id: int, unit_data: UnitCreate, creator: User):
        # TODO: check creator role
        return await crud_unit.create_for_module(db, module_id=module_id, obj_in=unit_data)

    async def get_units_for_module(self, db: AsyncSession, module_id: int, user: User):
        return await crud_unit.get_multi_by_module(db, module_id=module_id)

unit_service = UnitService()
