from pydantic import BaseModel
from typing import Optional


class LessonCreate(BaseModel):
    module_id: int
    title: str
    content: Optional[str]
    position: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "module_id": 1,
                "title": "Variables and Data Types",
                "content": "Learn about variables...",
                "position": 1,
            }
        }


class LessonUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    position: Optional[int]


class LessonOut(BaseModel):
    lesson_id: int
    module_id: int
    title: str
    content: Optional[str]
    position: Optional[int]

    class Config:
        orm_mode = True
