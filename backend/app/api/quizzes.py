from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.repositories.questions import QuestionsRepository
from app.schemas.questions import QuestionOut
from ..repositories.quizzes import QuizzesRepository
from ..schemas.quizzes import QuizCreate, QuizUpdate, QuizOut
from ..database.base import get_db
from ..repositories.user_progress import UserProgressRepository
from ..schemas.user_progress import UserProgressCreate

router = APIRouter()
quizzes_repository = QuizzesRepository()
questions_repository = QuestionsRepository()
progress_repository = UserProgressRepository()


@router.get("/lessons/{lesson_id}/quiz", response_model=QuizOut)
def get_quiz(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    quiz = quizzes_repository.get_lesson_quiz(db, lesson_id)

    questions = questions_repository.get_quiz_questions(db, quiz.quiz_id)

    questions_out = [QuestionOut.from_orm(question) for question in questions]

    # Create a QuizOut object using the quiz data and associated questions
    quiz_out = QuizOut(
        quiz_id=quiz.quiz_id,
        lesson_id=quiz.lesson_id,
        title=quiz.title,
        description=quiz.description,
        position=quiz.position,
        questions=questions_out,
    )

    return quiz_out


# Create a new quiz in a lesson
@router.post("/lessons/{lesson_id}/quiz", response_model=QuizOut)
def create_quiz(
    lesson_id: int,
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new quiz within a lesson.
    """
    new_quiz = quizzes_repository.create_quiz(db, lesson_id, quiz_data)
    return new_quiz


# Update a quiz
@router.patch("/quiz/{quiz_id}", response_model=QuizOut)
def update_quiz(
    quiz_id: int,
    quiz_data: QuizUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a quiz within a lesson.
    """
    updated_quiz = quizzes_repository.update_quiz(db, quiz_id, quiz_data)
    return updated_quiz


# Delete a quiz
@router.delete("/quiz/{quiz_id}")
def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a quiz within a lesson.
    """
    quizzes_repository.delete_quiz(db, quiz_id)
    return {"detail": "Quiz deleted successfully"}


@router.post("/lessons/{lesson_id}/quiz/submit")
def submit_quiz_results(
    user_id: int,
    lesson_id: int,
    correct_answers: int,
    total_questions: int,
    db: Session = Depends(get_db),
):
    progress_data = UserProgressCreate(
        user_id=user_id,
        lesson_id=lesson_id,
        correct_answers=correct_answers,
        total_questions=total_questions,
    )

    progress_repository.create_progress(db, progress_data)

    progress_repository.update_tokens_and_experience(db, user_id, correct_answers)

    return {"detail": "Quiz results submitted and progress updated successfully"}
