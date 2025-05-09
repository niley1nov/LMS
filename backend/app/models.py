# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID # Import UUID type for PostgreSQL
import uuid # Python's uuid module for default generation
from sqlalchemy.orm import relationship
from .database import Base # Assuming your Base is defined in database.py
import enum # Standard Python enum

# --- Enums ---
class UserRoleEnum(enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class UnitTypeEnum(enum.Enum):
    MATERIAL = "material"
    ASSIGNMENT = "assignment"
    QUIZ = "quiz"
    VIDEO = "video"
    DISCUSSION = "discussion"
    EXTERNAL_LINK = "external_link"

# --- Association Table (UserCourse) ---
class UserCourse(Base):
    __tablename__ = "user_courses"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    # Course ID in this table will now be a UUID to match Course.id
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    # create_type=False because the ENUM type 'user_course_role' is created by your DDL
    role = Column(SQLAlchemyEnum(UserRoleEnum, name="user_course_role", create_type=False), nullable=False)

    user = relationship("User", back_populates="course_associations")
    course = relationship("Course", back_populates="user_associations")

# --- Main Tables ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True) # User ID can remain integer
    google_sub = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)

    course_associations = relationship("UserCourse", back_populates="user", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = 'courses'
    # Change primary key to UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True) # Matches your DDL (was NOT NULL in your schema output)

    user_associations = relationship("UserCourse", back_populates="course", cascade="all, delete-orphan")
    modules = relationship(
        "Module",
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Module.order"
    )

class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True, index=True) # Module ID can remain integer for now
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True) # Using Text for consistency
    order = Column(Integer, nullable=False, default=0)

    # Course ID in this table will now be a UUID
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="modules")

    units = relationship(
        "Unit",
        back_populates="module",
        cascade="all, delete-orphan",
        order_by="Unit.order"
    )

class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True, index=True) # Unit ID can remain integer
    title = Column(String(255), nullable=False)
    # Explicitly state that the 'unit_type' attribute maps to the database column named 'type'.
    # create_type=False because the ENUM type 'unit_type_enum' is created by your DDL
    unit_type = Column("type", SQLAlchemyEnum(UnitTypeEnum, name="unit_type_enum", create_type=False), nullable=False)
    content = Column(Text, nullable=True)
    order = Column(Integer, nullable=False, default=0)

    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    module = relationship("Module", back_populates="units")
