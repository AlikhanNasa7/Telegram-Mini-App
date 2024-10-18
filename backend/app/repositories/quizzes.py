from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import Quiz
from ..schemas.quizzes import QuizCreate, QuizUpdate


class QuizzesRepository:
    def get_user_lesson_quiz(
        self, db: Session, user_id: int, course_id: int, module_id: int, lesson_id: int
    ) -> Quiz:
        quiz = db.query(Quiz).filter(Quiz.lesson_id == lesson_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        return quiz

    def create_quiz(
        self,
        db: Session,
        user_id: int,
        course_id: int,
        module_id: int,
        lesson_id: int,
        quiz_data: QuizCreate,
    ) -> Quiz:
        try:
            new_quiz = Quiz(
                lesson_id=lesson_id,
                title=quiz_data.title,
                description=quiz_data.description,
            )
            db.add(new_quiz)
            db.commit()
            db.refresh(new_quiz)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while creating quiz"
            )
        return new_quiz

    def update_quiz(
        self,
        db: Session,
        user_id: int,
        course_id: int,
        module_id: int,
        lesson_id: int,
        quiz_data: QuizUpdate,
    ) -> Quiz:
        try:
            quiz = self.get_user_lesson_quiz(
                db, user_id, course_id, module_id, lesson_id
            )
            for field, value in quiz_data.model_dump(exclude_unset=True).items():
                setattr(quiz, field, value)
            db.commit()
            db.refresh(quiz)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while updating quiz"
            )
        return quiz

    def delete_quiz(
        self, db: Session, user_id: int, course_id: int, module_id: int, lesson_id: int
    ):
        try:
            quiz = self.get_user_lesson_quiz(
                db, user_id, course_id, module_id, lesson_id
            )
            db.delete(quiz)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while deleting quiz"
            )
