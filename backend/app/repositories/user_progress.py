from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import UserProgress
from ..schemas.user_progress import UserProgressCreate, UserProgressUpdate
from ..repositories.users import UsersRepository


class UserProgressRepository:
    def get_user_progress(
        self, db: Session, user_id: int, lesson_id: int
    ) -> UserProgress:
        progress = (
            db.query(UserProgress)
            .filter(
                UserProgress.user_id == user_id, UserProgress.lesson_id == lesson_id
            )
            .first()
        )
        if not progress:
            raise HTTPException(status_code=404, detail="Progress not found")
        return progress

    def create_or_update_progress(
        self, db: Session, progress_data: UserProgressCreate
    ) -> UserProgress:
        try:
            progress = (
                db.query(UserProgress)
                .filter(
                    UserProgress.user_id == progress_data.user_id,
                    UserProgress.lesson_id == progress_data.lesson_id,
                )
                .first()
            )

            if progress:
                for field, value in progress_data.model_dump(
                    exclude_unset=True
                ).items():
                    setattr(progress, field, value)
            else:
                progress = UserProgress(**progress_data.model_dump())
                db.add(progress)

            db.commit()
            db.refresh(progress)

        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Error while updating progress")
        return progress

    def update_tokens_and_experience(
        self, db: Session, user_id: int, correct_answers: int, total_questions: int
    ):
        try:
            user_repo = UsersRepository()
            user = user_repo.get_user_by_id(db, user_id)

            # Calculate points and tokens
            experience_points_gain = (
                correct_answers * 10
            )  # Example: 10 XP per correct answer
            token_gain = correct_answers * 2  # Example: 2 tokens per correct answer

            user.experience_points += experience_points_gain
            user.tokens_balance += token_gain

            # Check if level should increase
            if (
                user.experience_points >= 100 * user.level
            ):  # Example: level up when XP reaches 100 * current level
                user.level += 1

            db.commit()
            db.refresh(user)

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Error while updating user tokens or experience"
            )
