# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean # Added Boolean for example
from sqlalchemy.orm import relationship

from .base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    google_sub = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    # is_active = Column(Boolean, default=True) # Example
    # is_superuser = Column(Boolean, default=False) # Example

    course_associations = relationship(
        "UserCourse",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email!r}, name={self.name!r})>"