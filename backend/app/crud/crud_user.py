# backend/app/crud/crud_user.py
from typing import Optional, Any, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base_crud import CRUDBase # Import the new base class
from app.models.user import User as UserModel
from app.schemas.user_schemas import UserCreate, UserUpdate

class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[UserModel]:
        """
        Get a user by email.
        """
        result = await db.execute(select(self.model).filter(self.model.email == email))
        return result.scalars().first()

    async def get_by_google_sub(self, db: AsyncSession, *, google_sub: str) -> Optional[UserModel]:
        """
        Get a user by Google subject ID.
        """
        result = await db.execute(select(self.model).filter(self.model.google_sub == google_sub))
        return result.scalars().first()

    async def create_with_google(
        self, db: AsyncSession, *, google_sub: str, email: str, name: Optional[str] = None
    ) -> UserModel:
        """
        Creates a new user specifically from Google OAuth information.
        This bypasses the generic 'create' if UserCreate schema doesn't fit Google data directly.
        """
        db_obj = self.model(
            google_sub=google_sub,
            email=email,
            name=name
            # Add other default fields if necessary, e.g., is_active=True
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_from_google(
        self, db: AsyncSession, *, db_obj: UserModel, email: str, name: Optional[str] = None
    ) -> UserModel:
        """
        Updates an existing user's details specifically from Google OAuth information.
        """
        update_data = {"email": email}
        if name is not None:
            update_data["name"] = name
        
        return await self.update(db, db_obj=db_obj, obj_in=update_data) # Use inherited update

    async def upsert_google_user(
        self, db: AsyncSession, *, google_sub: str, email: str, name: Optional[str]
    ) -> UserModel:
        """
        Gets an existing user by google_sub or creates a new one.
        Updates email and name if the user exists.
        """
        user = await self.get_by_google_sub(db, google_sub=google_sub)
        if user:
            update_payload = {}
            needs_update = False
            if user.email != email:
                update_payload["email"] = email
                needs_update = True
            if name is not None and user.name != name: # Only update name if provided and different
                update_payload["name"] = name
                needs_update = True
            
            if needs_update:
                user = await self.update(db, db_obj=user, obj_in=update_payload) # Use inherited update
        else:
            user = await self.create_with_google(db, google_sub=google_sub, email=email, name=name)
        return user

    # The generic create method from CRUDBase will be used if you call crud_user.create(db, obj_in=user_create_schema)
    # Ensure your UserCreate schema has all fields required by the UserModel constructor
    # or that your UserModel has appropriate defaults.
    # If UserCreate is very different from UserModel fields, you might override create:
    # async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> UserModel:
    #     db_obj = self.model(
    #         email=obj_in.email,
    #         name=obj_in.name,
    #         google_sub=obj_in.google_sub
    #     )
    #     db.add(db_obj)
    #     await db.commit()
    #     await db.refresh(db_obj)
    #     return db_obj


# Instantiate the CRUDUser class
crud_user = CRUDUser(UserModel)
