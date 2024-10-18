from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import Lesson
from ..schemas.lessons import LessonCreate, LessonUpdate


class LessonsRepository:
    def get_user_module_lessons(
        self, db: Session, user_id: int, course_id: int, module_id: int
    ) -> list[Lesson]:
        return db.query(Lesson).filter(Lesson.module_id == module_id).all()

    def get_user_module_lesson_by_id(
        self, db: Session, user_id: int, course_id: int, module_id: int, lesson_id: int
    ) -> Lesson:
        lesson = (
            db.query(Lesson)
            .filter(Lesson.module_id == module_id, Lesson.lesson_id == lesson_id)
            .first()
        )
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return lesson

    def create_lesson(
        self,
        db: Session,
        user_id: int,
        course_id: int,
        module_id: int,
        lesson_data: LessonCreate,
    ) -> Lesson:
        try:
            # Query the maximum position of existing lessons in the module
            max_position = (
                db.query(func.max(Lesson.position))
                .filter(Lesson.module_id == module_id)
                .scalar()
            )

            # Set the position to max_position + 1, or 1 if no lessons exist
            new_position = (max_position or 0) + 1

            # Create the new lesson with the calculated position
            new_lesson = Lesson(
                module_id=module_id,
                title=lesson_data.title,
                content=lesson_data.content,
                position=new_position,
            )
            db.add(new_lesson)
            db.commit()
            db.refresh(new_lesson)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while creating lesson"
            )
        return new_lesson

    def update_lesson(
        self,
        db: Session,
        user_id: int,
        course_id: int,
        module_id: int,
        lesson_id: int,
        lesson_data: LessonUpdate,
    ) -> Lesson:
        try:
            lesson = self.get_user_module_lesson_by_id(
                db, user_id, course_id, module_id, lesson_id
            )
            for field, value in lesson_data.model_dump(exclude_unset=True).items():
                setattr(lesson, field, value)
            db.commit()
            db.refresh(lesson)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while updating lesson"
            )
        return lesson

    def delete_lesson(
        self, db: Session, user_id: int, course_id: int, module_id: int, lesson_id: int
    ):
        try:
            lesson = self.get_user_module_lesson_by_id(
                db, user_id, course_id, module_id, lesson_id
            )
            db.delete(lesson)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while deleting lesson"
            )
