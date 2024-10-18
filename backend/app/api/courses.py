from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.courses import CoursesRepository
from ..schemas.courses import CourseCreate, CourseUpdate, CourseOut, Courses
from ..database.base import get_db
from ..llm import course_creator
import json


router = APIRouter()
courses_repository = CoursesRepository()


# Get all courses belonging to the user
@router.get("/", response_model=Courses)
def get_courses(
    db: Session = Depends(get_db),
    limit: int = 5,
    offset: int = 0,
):
    total_count, courses = courses_repository.get_courses(db, limit, offset)
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found")
    return Courses(
        total=total_count,
        objects=courses
    )


# Get a specific course belonging to the user
@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = courses_repository.get_course_by_id(db, course_id)
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


@router.post("/generate")
def generate_course(
    user_id: int, learning_field: str, description: str, db: Session = Depends(get_db)
):
    if description == "":
        raise HTTPException(status_code=400, detail="Description cannot be empty")

    if learning_field == "":
        raise HTTPException(status_code=400, detail="Course name cannot be empty")

    course_JSON = course_creator.create_course(learning_field, description)

    course_data = json.loads(course_JSON)

    return course_data
