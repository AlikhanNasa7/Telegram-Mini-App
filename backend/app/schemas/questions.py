from pydantic import BaseModel
from typing import Optional, List, Any


class QuestionCreate(BaseModel):
    question_text: str
    question_type: str  # 'multiple_choice', 'true_false'
    options: Optional[List[Any]]  # List of options for multiple-choice
    correct_answer: str

    class Config:
        schema_extra = {
            "example": {
                "quiz_id": 1,
                "question_text": "What is a variable?",
                "question_type": "multiple_choice",
                "options": ["A", "B", "C", "D"],
                "correct_answer": "A",
            }
        }


class QuestionUpdate(BaseModel):
    question_text: Optional[str]
    question_type: Optional[str]
    options: Optional[List[Any]]
    correct_answer: Optional[str]


class QuestionOut(BaseModel):
    question_id: int
    quiz_id: int
    question_text: str
    question_type: str
    options: Optional[List[Any]]
    correct_answer: str

    class Config:
        orm_mode = True
