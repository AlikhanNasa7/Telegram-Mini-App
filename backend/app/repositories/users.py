from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import User
from ..schemas.users import UserCreate, UserUpdate


class UsersRepository:
    def get_user_by_id(self, db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        try:
            new_user = User(
                user_id=user_data.user_id,
                username=user_data.username,
                tokens_balance=user_data.tokens_balance,
                experience_points=user_data.experience_points,
                level=user_data.level,
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while creating user"
            )
        return new_user

    def update_user(self, db: Session, user_id: int, user_data: UserUpdate) -> User:
        try:
            user = self.get_user_by_id(db, user_id)
            for field, value in user_data.model_dump(exclude_unset=True).items():
                setattr(user, field, value)
            db.commit()
            db.refresh(user)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while updating user"
            )
        return user

    def delete_user(self, db: Session, user_id: int):
        try:
            user = self.get_user_by_id(db, user_id)
            db.delete(user)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while deleting user"
            )
