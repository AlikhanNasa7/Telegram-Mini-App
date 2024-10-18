from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.courses import CoursesRepository
from ..schemas.courses import CourseCreate, CourseUpdate, CourseOut
from ..database.base import get_db

router = APIRouter()
courses_repository = CoursesRepository()


# Get all courses belonging to the user
@router.get("/", response_model=list[CourseOut])
def get_user_courses(user_id: int, db: Session = Depends(get_db)):
    courses = courses_repository.get_user_courses(db, user_id)
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found")
    return courses


# Get a specific course belonging to the user
@router.get("/{course_id}", response_model=CourseOut)
def get_course(user_id: int, course_id: int, db: Session = Depends(get_db)):
    course = courses_repository.get_user_course_by_id(db, user_id, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# Create a new course
@router.post("/", response_model=CourseOut)
def create_course(
    user_id: int, course_data: CourseCreate, db: Session = Depends(get_db)
):
    new_course = courses_repository.create_course(db, user_id, course_data)
    return new_course


# Update a course
@router.patch("/{course_id}", response_model=CourseOut)
def update_course(
    user_id: int,
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
):
    updated_course = courses_repository.update_course(
        db, user_id, course_id, course_data
    )
    return updated_course


# Delete a course
@router.delete("/{course_id}")
def delete_course(user_id: int, course_id: int, db: Session = Depends(get_db)):
    courses_repository.delete_course(db, user_id, course_id)
    return {"detail": "Course deleted successfully"}
