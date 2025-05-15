# backend/app/api/v1/endpoints/modules.py
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import traceback
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from app.db.session import get_db_session
from app.models.user import User as UserModel
from app.services.module_service import module_service
from app.schemas.module_schemas import ModuleCreate, ModuleOut
from app.api.deps import get_current_active_user

router = APIRouter()

@router.post(
    "",
    response_model=ModuleOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new module in a course",
)
async def create_module_for_course(
    course_id: uuid.UUID,
    module_in: ModuleCreate,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(get_current_active_user),
):
    """
    Create a new module under the given course.
    Only teachers/admins may call this.
    """
    try:
        module = await module_service.create_module(
            db, course_id=course_id, module_data=module_in, creator=current_user
        )
        # --- Explicitly validate the returned ORM against Pydantic ---
        return ModuleOut.model_validate(module)
    except HTTPException:
        raise
    except IntegrityError as ie:
        # detect your unique‐constraint name
        if "uq_module_course_order" in str(ie.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Module order {module_in.order} is already in use for this course.",
            )
        # otherwise fall through
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database integrity error: {ie.orig}",
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating module: {e}",
        )

@router.get(
    "",
    response_model=List[ModuleOut],
    summary="List modules for a course",
)
async def list_modules_of_course(
    course_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
    current_user: UserModel = Depends(get_current_active_user),
):
    return await module_service.get_modules_for_course(db, course_id, current_user)
