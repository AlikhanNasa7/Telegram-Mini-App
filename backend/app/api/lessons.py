import os
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..repositories.lessons import LessonsRepository
from ..schemas.lessons import LessonCreate, LessonUpdate, LessonOut
from ..database.base import get_db

router = APIRouter()
lessons_repository = LessonsRepository()


# Get all lessons within a specific module
@router.get("/modules/{module_id}/lessons", response_model=list[LessonOut])
def get_module_lessons(module_id: int, db: Session = Depends(get_db)):
    lessons = lessons_repository.get_module_lessons(db, module_id)
    if not lessons:
        return Response(status_code=200, content="No modules found")
    return lessons


# Get a specific lesson within a module
@router.get("/lessons/{lesson_id}", response_model=LessonOut)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    lesson = lessons_repository.get_module_lesson_by_id(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson


# Create a new lesson in a module
@router.post("/modules/{module_id}/lessons", response_model=LessonOut)
def create_lesson(
    module_id: int,
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
):
    new_lesson = lessons_repository.create_lesson(db, module_id, lesson_data)
    return new_lesson


# Update a lesson
@router.patch("/lessons/{lesson_id}", response_model=LessonOut)
def update_lesson(
    lesson_id: int,
    lesson_data: LessonUpdate,
    db: Session = Depends(get_db),
):
    updated_lesson = lessons_repository.update_lesson(db, lesson_id, lesson_data)
    return updated_lesson


# Delete a lesson
@router.delete("/lessons/{lesson_id}")
def delete_lesson(
    module_id: int,
    lesson_id: int,
    db: Session = Depends(get_db),
):
    lessons_repository.delete_lesson(db, module_id, lesson_id)
    return {"detail": "Lesson deleted successfully"}


@router.get("/lessons/{lesson_id}/audio", response_class=FileResponse)
def get_audio_for_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    """
    Получает аудиофайл для указанного урока.
    """
    lesson = lessons_repository.get_module_lesson_by_id(db, lesson_id)

    if not lesson.audio_file_path or not os.path.exists(lesson.audio_file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(
        path=lesson.audio_file_path,
        media_type="audio/mpeg",
        filename=os.path.basename(lesson.audio_file_path),
    )