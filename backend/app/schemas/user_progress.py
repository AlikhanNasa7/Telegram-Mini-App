from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserProgressCreate(BaseModel):
    user_id: int
    lesson_id: int
    correct_answers: int = 0
    total_questions: int = 0


class UserProgressUpdate(BaseModel):
    status: Optional[str]
    score: Optional[float]
    attempts: Optional[int]


class UserProgressOut(BaseModel):
    progress_id: int
    user_id: int
    lesson_id: Optional[int]
    quiz_id: Optional[int]
    status: str
    score: Optional[float]
    last_accessed: datetime
    attempts: int

    class Config:
        orm_mode = True
