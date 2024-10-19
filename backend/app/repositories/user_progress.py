from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import UserProgress
from ..schemas.user_progress import UserProgressCreate, UserProgressUpdate
from ..repositories.users import UsersRepository


REWARD_TOKENS = 50


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
            return None
        return progress

    def create_progress(
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
                raise HTTPException(
                    status_code=400, detail="Progress already exists for this lesson"
                )
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
        self, db: Session, user_id: int, correct_answers: int
    ):
        try:
            user_repo = UsersRepository()
            user = user_repo.get_user_by_id(db, user_id)

            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            experience_points_gain = correct_answers * 10
            token_gain = correct_answers * REWARD_TOKENS

            user.experience_points += experience_points_gain
            user.tokens_balance += token_gain

            if user.experience_points >= 100 * user.level:
                user.level += 1

            db.commit()
            db.refresh(user)

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Error while updating user tokens or experience"
            )
