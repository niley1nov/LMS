from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from .database import Base # Assuming your Base is defined in database.py
import enum # Standard Python enum

# Define the Role enum using Python's enum class
# This will be used by SQLAlchemy's Enum type
class UserRoleEnum(enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

# Association table for the many-to-many relationship
# between Users and Courses, including the role.
class UserCourse(Base):
    __tablename__ = "user_courses"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    # Use SQLAlchemyEnum, linking to the Python enum and specifying native enum options for PostgreSQL
    role = Column(SQLAlchemyEnum(UserRoleEnum, name="user_course_role", create_type=True), nullable=False)

    # Relationships to easily access User and Course from a UserCourse instance
    user = relationship("User", back_populates="course_associations")
    course = relationship("Course", back_populates="user_associations")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    google_sub = Column(String, unique=True, index=True, nullable=False) # Assuming this was intended
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)

    # Relationship to UserCourse (one-to-many: one User can have many entries in UserCourse)
    # This allows us to get all (course, role) pairs for a user.
    course_associations = relationship("UserCourse", back_populates="user", cascade="all, delete-orphan")

    # If you want a direct list of Course objects for a user (without easily getting the role directly from here):
    # courses = relationship("Course", secondary="user_courses", back_populates="users")
    # However, using course_associations is more explicit for getting roles.

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)

    # Relationship to UserCourse (one-to-many: one Course can have many entries in UserCourse)
    # This allows us to get all (user, role) pairs for a course.
    user_associations = relationship("UserCourse", back_populates="course", cascade="all, delete-orphan")

    # If you want a direct list of User objects for a course:
    # users = relationship("User", secondary="user_courses", back_populates="courses")
