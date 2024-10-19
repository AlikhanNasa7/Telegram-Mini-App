from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.users import UsersRepository
from ..schemas.users import UserOut, UserCreate
from ..schemas.courses import CourseOut, Courses
from ..database.base import get_db

router = APIRouter()
users_repository = UsersRepository()


@router.post("/", response_model=UserOut)
def create_or_return_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = users_repository.get_user_by_id(db, user_data.user_id)
    if user:
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


# Delete user account
@router.delete("/")
def delete_current_user(user_id: int, db: Session = Depends(get_db)):
    users_repository.delete_user(db, user_id)
    return {"detail": "User deleted successfully"}


# Get all courses of user
@router.get("/created-courses", response_model=Courses)
def get_created_courses_of_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    total_count, courses = users_repository.get_courses_created_by_user(
        db, user_id=user_id
    )
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found")
    return Courses(total=total_count, objects=courses)


@router.get("/enrolled-courses", response_model=List[CourseOut])
def get_enrolled_courses_of_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    # Get the user by ID
    user = users_repository.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Access the enrolled courses via the relationship
    enrolled_courses = user.enrolled_courses

    if not enrolled_courses:
        raise HTTPException(
            status_code=404, detail="No enrolled courses found for this user"
        )

    # Print each enrolled course for debugging purposes
    for course in enrolled_courses:
        print(course)

    # Return the list of enrolled courses
    return [
        course.course for course in enrolled_courses
    ]  # Access the related Course object
