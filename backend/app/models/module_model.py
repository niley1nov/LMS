# backend/app/models/module_model.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base_class import Base

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=False, default=0)

    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="modules")

    units = relationship(
        "Unit",
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="Unit.order"
    )

    def __repr__(self):
        return f"<Module(id={self.id}, title={self.title!r}, course_id={self.course_id})>"
