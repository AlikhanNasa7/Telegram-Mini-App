from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CourseCreate(BaseModel):
    title: str
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Python Basics",
                "description": "An introductory course on Python programming.",
            }
        }


class CourseUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]


class CourseOut(BaseModel):
    course_id: int
    user_id: int
    title: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
