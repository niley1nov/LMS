# backend/app/api/v1/endpoints/units.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import traceback
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from app.db.session import get_db_session
from app.models.user import User as UserModel
from app.services.unit_service import unit_service
from app.schemas.unit_schemas import UnitCreate, UnitOut
from app.api.deps import get_current_active_user

router = APIRouter()

@router.post(
    "",
    response_model=UnitOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new unit in a module",
)
async def create_unit_for_module(
    module_id: int,
    unit_in: UnitCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(get_current_active_user),
):
    """
    Create a new unit (material/quiz/etc) under the given module.
    """
    try:
        # 1) create
        unit = await unit_service.create_unit(
            db, module_id=module_id, unit_data=unit_in, creator=current_user
        )
        # 2) validate against Pydantic, catching any missing‐relationship issues
        try:
            validated = UnitOut.model_validate(unit)
        except ValidationError as ve:
            traceback.print_exc()
            msgs = "; ".join(err["msg"] for err in ve.errors())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal serialization error: {msgs}",
            )

        return validated
    except HTTPException:
        raise
    except IntegrityError as ie:
        # catch your module‐unit‐order unique constraint (if you have one)
        if "uq_unit_module_order" in str(ie.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unit order {unit_in.order} is already in use for this module.",
            )
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {ie.orig}",
        )
    except Exception as e:
        traceback.print_exc()
        # bubble up the real exception message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating unit: {e}",
        )

@router.get(
    "",
    response_model=List[UnitOut],
    summary="List units for a module",
)
async def list_units_of_module(
    module_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(get_current_active_user),
):
    return await unit_service.get_units_for_module(db, module_id, current_user)
