# backend/app/crud/base_crud.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
import traceback

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.base_class import Base as SABase

ModelType = TypeVar("ModelType", bound=SABase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticBaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        # Use bltns.id() if you ever shadow 'id' locally and need the built-in
        # import builtins as bltns
        print(f"DEBUG: CRUDBase instance {id(self)} initialized for model: {model.__name__}")

    async def get(self, db: AsyncSession, record_id: Any) -> Optional[ModelType]: # Renamed 'id' to 'record_id'
        # Use builtins.id if 'id' is ever shadowed in this scope and you need the function
        # import builtins as bltns
        print(f"DEBUG: ***** INSIDE CRUDBase.get (instance {id(self)}) for model {self.model.__name__} with record_id: {record_id} (type: {type(record_id)}) *****")
        try:
            current_id_param = record_id # Use the renamed parameter

            # Type check for User model ID specifically
            if self.model.__name__ == "User" and not isinstance(current_id_param, int):
                 print(f"WARNING: CRUDBase.get for User model received non-integer record_id: {current_id_param} (type: {type(current_id_param)})")
                 try:
                     current_id_param = int(current_id_param)
                     print(f"DEBUG: Converted record_id to int for User query: {current_id_param}")
                 except ValueError:
                     print(f"ERROR: Cannot convert record_id '{current_id_param}' to int for User model query.")
                     return None

            stmt = select(self.model).filter(self.model.id == current_id_param) # Use current_id_param
            print(f"DEBUG: CRUDBase.get - Executing statement: {str(stmt)}")
            result = await db.execute(stmt)
            scalar_result = result.scalars().first()
            print(f"DEBUG: ***** CRUDBase.get query result for record_id {current_id_param}: {'Found object with ID ' + str(scalar_result.id) if scalar_result and hasattr(scalar_result, 'id') else 'None'} *****")
            if scalar_result:
                print(f"DEBUG: Object details from CRUDBase.get: {scalar_result}")
            return scalar_result
        except Exception as e:
            print(f"CRITICAL ERROR in CRUDBase.get (instance {id(self)} for model {self.model.__name__}, record_id {record_id}): {e}")
            traceback.print_exc()
            return None

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        print(f"DEBUG: CRUDBase.get_multi (instance {id(self)}) called for model {self.model.__name__}.")
        try:
            stmt = select(self.model).offset(skip).limit(limit)
            if hasattr(self.model, 'id'):
                stmt = stmt.order_by(self.model.id)
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            print(f"ERROR in CRUDBase.get_multi: {e}")
            traceback.print_exc()
            return []


    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        print(f"DEBUG: CRUDBase.create (instance {id(self)}) called for model {self.model.__name__}.")
        try:
            obj_in_data = obj_in.model_dump()
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except Exception as e:
            print(f"ERROR in CRUDBase.create: {e}")
            traceback.print_exc()
            raise

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        print(f"DEBUG: CRUDBase.update (instance {id(self)}) called for model {self.model.__name__}, obj ID: {db_obj.id if hasattr(db_obj, 'id') else 'N/A'}.")
        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except Exception as e:
            print(f"ERROR in CRUDBase.update: {e}")
            traceback.print_exc()
            raise

    async def remove(self, db: AsyncSession, *, record_id: Any) -> Optional[ModelType]: # Renamed 'id' to 'record_id'
        print(f"DEBUG: CRUDBase.remove (instance {id(self)}) called for model {self.model.__name__}, record_ID: {record_id}.")
        try:
            obj = await self.get(db, record_id=record_id) # Use the renamed parameter here
            if obj:
                await db.delete(obj)
                await db.commit()
                return obj
            return None
        except Exception as e:
            print(f"ERROR in CRUDBase.remove: {e}")
            traceback.print_exc()
            return None