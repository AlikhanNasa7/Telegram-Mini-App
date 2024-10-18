from pydantic import BaseModel
from typing import Optional


class QuizCreate(BaseModel):
    title: str
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Quiz on Variables",
                "description": "Test your knowledge on variables.",
            }
        }


class QuizUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    position: Optional[int]


class QuizOut(BaseModel):
    quiz_id: int
    lesson_id: int
    title: str
    description: Optional[str]
    position: Optional[int]

    class Config:
        orm_mode = True
