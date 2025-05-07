from pydantic import BaseModel

class CourseOut(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
