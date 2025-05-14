# backend/app/models/course.py
from sqlalchemy import Column, Text, ForeignKey, Integer # Added ForeignKey, Integer for example
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from .base_class import Base
# from .user import User # If you had created_by relationship

class Course(Base):
    __tablename__ = 'courses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    # created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # created_by = relationship("User")

    user_associations = relationship(
        "UserCourse",
        back_populates="course",
        cascade="all, delete-orphan"
    )

    modules = relationship(
        "Module",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Module.order"
    )

    def __repr__(self):
        return f"<Course(id={self.id}, name={self.name!r})>"
