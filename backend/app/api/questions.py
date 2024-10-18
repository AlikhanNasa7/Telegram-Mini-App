from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.questions import QuestionsRepository
from ..schemas.questions import QuestionCreate, QuestionUpdate, QuestionOut
from ..database.base import get_db

router = APIRouter()
questions_repository = QuestionsRepository()


# Get all questions within a quiz
@router.get("/", response_model=list[QuestionOut])
def get_quiz_questions(
    course_id: int,
    module_id: int,
    lesson_id: int,
    quiz_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    questions = questions_repository.get_user_quiz_questions(
        db, user_id, course_id, module_id, lesson_id, quiz_id
    )
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found in this quiz")
    return questions


# Get a specific question within a quiz
@router.get("/{question_id}", response_model=QuestionOut)
def get_question(
    course_id: int,
    module_id: int,
    lesson_id: int,
    quiz_id: int,
    question_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    question = questions_repository.get_user_quiz_question_by_id(
        db, user_id, course_id, module_id, lesson_id, quiz_id, question_id
    )
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


# Create a new question in a quiz
@router.post("/", response_model=QuestionOut)
def create_question(
    course_id: int,
    module_id: int,
    lesson_id: int,
    quiz_id: int,
    user_id: int,
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
):
    new_question = questions_repository.create_question(
        db, user_id, course_id, module_id, lesson_id, quiz_id, question_data
    )
    return new_question


# Update a question
@router.patch("/{question_id}", response_model=QuestionOut)
def update_question(
    course_id: int,
    module_id: int,
    lesson_id: int,
    quiz_id: int,
    question_id: int,
    user_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
):
    updated_question = questions_repository.update_question(
        db,
        user_id,
        course_id,
        module_id,
        lesson_id,
        quiz_id,
        question_id,
        question_data,
    )
    return updated_question


# Delete a question
@router.delete("/{question_id}")
def delete_question(
    course_id: int,
    module_id: int,
    lesson_id: int,
    quiz_id: int,
    question_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    questions_repository.delete_question(
        db, user_id, course_id, module_id, lesson_id, quiz_id, question_id
    )
    return {"detail": "Question deleted successfully"}
