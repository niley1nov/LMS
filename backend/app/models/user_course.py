# backend/app/models/user_course.py
from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base_class import Base
from .enums import UserCourseRoleEnum

class UserCourse(Base):
    __tablename__ = "user_courses"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    role = Column(
        SQLAlchemyEnum(UserCourseRoleEnum, name="user_course_role", create_type=False),
        nullable=False
    )

    user = relationship("User", back_populates="course_associations")
    course = relationship("Course", back_populates="user_associations")

    def __repr__(self):
        role_value = self.role.value if self.role else None
        user_id_val = self.user.id if self.user else self.user_id # Fallback to id if user object not loaded
        course_id_val = self.course.id if self.course else self.course_id # Fallback
        return f"<UserCourse(user_id={user_id_val}, course_id={course_id_val}, role={role_value!r})>"
