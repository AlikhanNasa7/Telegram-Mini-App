from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import Quiz
from ..schemas.quizzes import QuizCreate, QuizUpdate


from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


class QuizzesRepository:

    def get_lesson_quiz(self, db: Session, lesson_id: int) -> Quiz:
        quiz = db.query(Quiz).filter(Quiz.lesson_id == lesson_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        return quiz

    def create_quiz(
        self,
        db: Session,
        lesson_id: int,
        quiz_data: QuizCreate,
    ) -> Quiz:
        try:
            # Check if a quiz already exists for the lesson
            existing_quiz = db.query(Quiz).filter(Quiz.lesson_id == lesson_id).first()
            if existing_quiz:
                raise HTTPException(
                    status_code=400, detail="A quiz already exists for this lesson"
                )

            # Create the new quiz
            new_quiz = Quiz(
                lesson_id=lesson_id,
                title=quiz_data.title,
                description=quiz_data.description,
                position=1,  # Position is set to 1 because only one quiz is allowed per lesson
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
        quiz_id: int,
        quiz_data: QuizUpdate,
    ) -> Quiz:
        try:
            quiz = self.get_quiz(db, quiz_id)
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

    def delete_quiz(self, db: Session, quiz_id: int):
        try:
            quiz = self.get_quiz(db, quiz_id)
            if not quiz:
                raise HTTPException(status_code=404, detail="Quiz not found")
            db.delete(quiz)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while deleting quiz"
            )
