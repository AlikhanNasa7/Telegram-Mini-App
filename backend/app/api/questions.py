from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from ..repositories.questions import QuestionsRepository
from ..schemas.questions import QuestionCreate, QuestionUpdate, QuestionOut
from ..database.base import get_db

router = APIRouter()
questions_repository = QuestionsRepository()


# Get all questions within a quiz
@router.get("/quizzes/{quiz_id}/questions", response_model=list[QuestionOut])
def get_quiz_questions(
    quiz_id: int,
    db: Session = Depends(get_db),
):
    questions = questions_repository.get_quiz_questions(db, quiz_id)
    if not questions:
        return Response(status_code=200, content="No modules found")
    return questions


# Get a specific question within a quiz
@router.get("/questions/{question_id}", response_model=QuestionOut)
def get_question(
    quiz_id: int,
    question_id: int,
    db: Session = Depends(get_db),
):
    question = questions_repository.get_question_by_id(db, quiz_id, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


# Create a new question in a quiz
@router.post("/quizzes/{quiz_id}/questions", response_model=QuestionOut)
def create_question(
    quiz_id: int,
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
):
    new_question = questions_repository.create_question(db, quiz_id, question_data)
    return new_question


# Update a question
@router.patch("/questions/{question_id}", response_model=QuestionOut)
def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
):
    updated_question = questions_repository.update_question(
        db,
        question_id,
        question_data,
    )
    return updated_question


# Delete a question
@router.delete("/questions/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
):
    questions_repository.delete_question(db, question_id)
    return {"detail": "Question deleted successfully"}
