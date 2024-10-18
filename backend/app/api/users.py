from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.users import UsersRepository
from ..schemas.users import UserOut, UserCreate
from ..schemas.courses import Courses
from ..database.base import get_db

router = APIRouter()
users_repository = UsersRepository()


@router.post("/", response_model=UserOut)
def create_or_update_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = users_repository.get_user_by_id(db, user_data.id)
    if user:
        user = users_repository.update_user(db, user_data)
        return user
    user = users_repository.create_user(db, user_data)
    return user


# Get current user profile
@router.get("/me", response_model=UserOut)
def get_current_user(user_id: int, db: Session = Depends(get_db)):
    user = users_repository.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Get all courses of user
@router.get("/courses", response_model=Courses)
def get_courses_of_user(
    user_id: int,
    db: Session = Depends(get_db),
    limit: int = 5,
    offset: int = 0,
):
    total_count, courses = users_repository.get_courses_by_user_id(
        db, limit, offset, user_id=user_id
    )
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found")
    return Courses(total=total_count, objects=courses)


# Delete user account
@router.delete("/")
def delete_current_user(user_id: int, db: Session = Depends(get_db)):
    users_repository.delete_user(db, user_id)
    return {"detail": "User deleted successfully"}
