# backend/app/models/unit.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from .base_class import Base
from .enums import UnitTypeEnum

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    unit_type = Column(
        "type",
        SQLAlchemyEnum(UnitTypeEnum, name="unit_type_enum_db", create_type=False), # Ensure this enum type name matches DB
        nullable=False
    )
    content = Column(Text, nullable=True)
    order = Column(Integer, nullable=False, default=0)

    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    module = relationship("Module", back_populates="units")

    def __repr__(self):
        type_value = self.unit_type.value if self.unit_type else None
        return f"<Unit(id={self.id}, title={self.title!r}, type={type_value!r}, module_id={self.module_id})>"
