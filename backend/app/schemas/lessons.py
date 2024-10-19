from pydantic import BaseModel
from typing import Optional, List, Any


class LessonCreate(BaseModel):
    title: str
    description: Optional[str]
    content: Optional[List[Any]]
    image_url: Optional[Any] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Variables and Data Types",
                "content": "Learn about variables...",
            }
        }


class LessonUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    content: Optional[List[Any]]
    position: Optional[int]
    image_url: Optional[Any]


class LessonOut(BaseModel):
    lesson_id: int
    module_id: int
    title: str
    description: Optional[str]
    position: Optional[int]
    content: Optional[List[Any]]
    image_url: Optional[Any]
    audio_file_path: Optional[Any]

    class Config:
        orm_mode = True
