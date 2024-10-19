from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserProgressCreate(BaseModel):
    user_id: int
    lesson_id: Optional[int]
    quiz_id: Optional[int]
    status: str  # 'not_started', 'in_progress', 'completed'
    score: Optional[float] = 0.0
    attempts: Optional[int] = 0

    class Config:
        schema_extra = {
            "example": {
                "user_id": 123456789,
                "lesson_id": 1,
                "quiz_id": None,
                "status": "in_progress",
                "score": 0.0,
                "attempts": 1,
            }
        }


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
