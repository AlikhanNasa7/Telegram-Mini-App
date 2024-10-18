from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.user_progress import UserProgressRepository
from ..schemas.user_progress import UserProgressCreate
from ..database.base import get_db

router = APIRouter()
progress_repository = UserProgressRepository()


# Endpoint to submit quiz results and update progress
@router.post("/submit")
def submit_quiz_results(
    user_id: int,
    lesson_id: int,
    correct_answers: int,
    total_questions: int,
    db: Session = Depends(get_db),
):
    # Create or update progress
    progress_data = UserProgressCreate(
        user_id=user_id,
        lesson_id=lesson_id,
        quiz_id=None,  # Assuming only one quiz per lesson
        status="completed",
        score=correct_answers / total_questions * 100,
        attempts=1,  # Increment attempts if needed
    )

    progress_repository.create_or_update_progress(db, progress_data)

    # Update tokens and experience points based on quiz performance
    progress_repository.update_tokens_and_experience(
        db, user_id, correct_answers, total_questions
    )

    return {"detail": "Quiz results submitted and progress updated successfully"}
