from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.users import UsersRepository
from ..schemas.users import UserOut, UserUpdate
from ..database.base import get_db

router = APIRouter()
users_repository = UsersRepository()


# Get current user profile
@router.get("/me", response_model=UserOut)
def get_current_user(user_id: int, db: Session = Depends(get_db)):
    user = users_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update current user profile
@router.patch("/me", response_model=UserOut)
def update_current_user(
    user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)
):
    updated_user = users_repository.update_user(db, user_id, user_data)
    return updated_user


# Delete user account
@router.delete("/me")
def delete_current_user(user_id: int, db: Session = Depends(get_db)):
    users_repository.delete_user(db, user_id)
    return {"detail": "User deleted successfully"}
