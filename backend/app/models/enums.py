# backend/app/models/enums.py
import enum

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

# Enum for the role within a course, used in UserCourse association
class UserCourseRoleEnum(enum.Enum):
    teacher = "teacher"
    student = "student"
    # Add other roles if needed, e.g., teaching_assistant