from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.quizzes import QuizzesRepository
from ..schemas.quizzes import QuizCreate, QuizUpdate, QuizOut
from ..database.base import get_db

from ..repositories.user_progress import UserProgressRepository
from ..schemas.user_progress import UserProgressCreate

router = APIRouter()
quizzes_repository = QuizzesRepository()
progress_repository = UserProgressRepository()


# Get all quizzes within a lesson
@router.get("/", response_model=list[QuizOut])
def get_lesson_quizzes(
    course_id: int,
    module_id: int,
    lesson_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    quizzes = quizzes_repository.get_user_lesson_quizzes(
        db, user_id, course_id, module_id, lesson_id
    )
    if not quizzes:
        raise HTTPException(status_code=404, detail="No quizzes found in this lesson")
    return quizzes


# Create a new quiz in a lesson
@router.post("/", response_model=QuizOut)
def create_quiz(
    course_id: int,
    module_id: int,
    lesson_id: int,
    user_id: int,
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
):
    new_quiz = quizzes_repository.create_quiz(
        db, user_id, course_id, module_id, lesson_id, quiz_data
    )
    return new_quiz


# Update a quiz
@router.patch("/{quiz_id}", response_model=QuizOut)
def update_quiz(
    course_id: int,
    module_id: int,
    lesson_id: int,
    quiz_id: int,
    user_id: int,
    quiz_data: QuizUpdate,
    db: Session = Depends(get_db),
):
    updated_quiz = quizzes_repository.update_quiz(
        db, user_id, course_id, module_id, lesson_id, quiz_id, quiz_data
    )
    return updated_quiz


# Delete a quiz
@router.delete("/{quiz_id}")
def delete_quiz(
    course_id: int,
    module_id: int,
    lesson_id: int,
    quiz_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    quizzes_repository.delete_quiz(
        db, user_id, course_id, module_id, lesson_id, quiz_id
    )
    return {"detail": "Quiz deleted successfully"}


@router.post("/{quiz_id}/submit")
def submit_quiz_results(
    user_id: int,
    quiz_id: int,
    lesson_id: int,  # Associated lesson ID
    correct_answers: int,
    total_questions: int,
    db: Session = Depends(get_db),
):
    """
    Submit the quiz results for the lesson and update user progress and experience.
    """

    # Step 1: Create or update progress for this quiz submission
    progress_data = UserProgressCreate(
        user_id=user_id,
        lesson_id=lesson_id,
        quiz_id=quiz_id,
        status="completed" if correct_answers == total_questions else "in_progress",
        score=(correct_answers / total_questions) * 100,  # Calculate percentage score
        attempts=1,  # This can be updated based on your app's logic (e.g., tracking attempts)
    )

    progress_repository.create_or_update_progress(db, progress_data)

    # Step 2: Update tokens and experience points based on quiz performance
    progress_repository.update_tokens_and_experience(
        db, user_id, correct_answers, total_questions
    )

    return {"detail": "Quiz results submitted and progress updated successfully"}
