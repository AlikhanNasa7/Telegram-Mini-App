from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import Lesson
from ..schemas.lessons import LessonCreate, LessonUpdate
from ..tts.tts import generate_audio
import uuid
from typing import Optional
import asyncio


class LessonsRepository:
    def get_module_lessons(self, db: Session, module_id: int) -> list[Lesson]:
        return db.query(Lesson).filter(Lesson.module_id == module_id).all()

    def get_module_lesson_by_id(self, db: Session, lesson_id: int) -> Lesson:
        lesson = db.query(Lesson).filter(Lesson.lesson_id == lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        return lesson

    def create_lesson(
        self,
        db: Session,
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
                description=lesson_data.description,
                content=lesson_data.content,
                position=new_position,
                image_url=lesson_data.image_url,
            )
            db.add(new_lesson)
            db.commit()
            db.refresh(new_lesson)

            if new_lesson.content:
                text = extract_text_from_content(new_lesson.content)
                if text:
                    filename = (
                        f"lesson_{new_lesson.lesson_id}_{uuid.uuid4().hex[:8]}.mp3"
                    )
                    audio_path = asyncio.run(
                        generate_and_save_audio(text, "en-US-GuyNeural", filename)
                    )
                    new_lesson.audio_file_path = str(audio_path)
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
        lesson_id: int,
        lesson_data: LessonUpdate,
    ) -> Lesson:
        try:
            lesson = self.get_module_lesson_by_id(db, lesson_id)
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

    def delete_lesson(self, db: Session, lesson_id: int):
        try:
            lesson = self.get_module_lesson_by_id(db, lesson_id)
            db.delete(lesson)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while deleting lesson"
            )


def extract_text_from_content(content: list) -> Optional[str]:
    """
    Извлекает текст из поля content.
    Предполагается, что content представляет собой список словарей с ключами 'type' и 'value'.
    """
    texts = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text" and "value" in item:
            texts.append(item["value"])
    return " ".join(texts) if texts else None


async def generate_and_save_audio(text: str, voice: str, filename: str) -> str:
    """
    Генерирует аудиофайл и сохраняет его в файловой системе.

    Args:
        text (str): Текст для преобразования в речь.
        voice (str): Выбранный голос для TTS.
        filename (str): Имя файла для сохранения.

    Returns:
        str: Путь к сохраненному аудиофайлу.
    """
    from ..tts.tts import (
        generate_audio,
    )  # Импорт внутри функции для избежания циклических импортов

    audio_path = await generate_audio(text, voice, filename)
    return audio_path
