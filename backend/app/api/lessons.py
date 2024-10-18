from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.lessons import LessonsRepository
from ..schemas.lessons import LessonCreate, LessonUpdate, LessonOut
from ..database.base import get_db

router = APIRouter()
lessons_repository = LessonsRepository()


# Get all lessons within a specific module
@router.get("/", response_model=list[LessonOut])
def get_module_lessons(
    course_id: int, module_id: int, user_id: int, db: Session = Depends(get_db)
):
    lessons = lessons_repository.get_user_module_lessons(
        db, user_id, course_id, module_id
    )
    if not lessons:
        raise HTTPException(status_code=404, detail="No lessons found in this module")
    return lessons


# Get a specific lesson within a module
@router.get("/{lesson_id}", response_model=LessonOut)
def get_lesson(
    course_id: int,
    module_id: int,
    lesson_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    lesson = lessons_repository.get_user_module_lesson_by_id(
        db, user_id, course_id, module_id, lesson_id
    )
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


# Create a new lesson in a module
@router.post("/", response_model=LessonOut)
def create_lesson(
    course_id: int,
    module_id: int,
    user_id: int,
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
):
    new_lesson = lessons_repository.create_lesson(
        db, user_id, course_id, module_id, lesson_data
    )
    return new_lesson


# Update a lesson
@router.patch("/{lesson_id}", response_model=LessonOut)
def update_lesson(
    course_id: int,
    module_id: int,
    lesson_id: int,
    user_id: int,
    lesson_data: LessonUpdate,
    db: Session = Depends(get_db),
):
    updated_lesson = lessons_repository.update_lesson(
        db, user_id, course_id, module_id, lesson_id, lesson_data
    )
    return updated_lesson


# Delete a lesson
@router.delete("/{lesson_id}")
def delete_lesson(
    course_id: int,
    module_id: int,
    lesson_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    lessons_repository.delete_lesson(db, user_id, course_id, module_id, lesson_id)
    return {"detail": "Lesson deleted successfully"}
