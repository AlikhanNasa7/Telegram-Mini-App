from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import Quiz
from ..schemas.quizzes import QuizCreate, QuizUpdate


class QuizzesRepository:
    def get_user_lesson_quizzes(
        self, db: Session, user_id: int, lesson_id: int
    ) -> list[Quiz]:
        quizzes = db.query(Quiz).filter(Quiz.lesson_id == lesson_id).all()
        if not quizzes:
            raise HTTPException(
                status_code=404, detail="No quizzes found in this lesson"
            )
        return quizzes

    def get_user_lesson_quiz(
        self, db: Session, user_id: int, lesson_id: int, quiz_id: int
    ) -> Quiz:
        quiz = (
            db.query(Quiz)
            .filter(Quiz.lesson_id == lesson_id, Quiz.quiz_id == quiz_id)
            .first()
        )
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        return quiz

    def create_quiz(
        self,
        db: Session,
        user_id: int,
        lesson_id: int,
        quiz_data: QuizCreate,
    ) -> Quiz:
        try:
            # Get the maximum position value for the quizzes in the lesson
            max_position = (
                db.query(func.max(Quiz.position))
                .filter(Quiz.lesson_id == lesson_id)
                .scalar()
            )

            # Set the position as max_position + 1, or 1 if no quizzes exist
            new_position = (max_position or 0) + 1

            # Create the new quiz with the calculated position
            new_quiz = Quiz(
                lesson_id=lesson_id,
                title=quiz_data.title,
                description=quiz_data.description,
                position=new_position,
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
        lesson_id: int,
        quiz_id: int,
        quiz_data: QuizUpdate,
    ) -> Quiz:
        try:
            quiz = self.get_user_lesson_quiz(db, user_id, lesson_id, quiz_id)
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

    def delete_quiz(self, db: Session, user_id: int, lesson_id: int, quiz_id: int):
        try:
            quiz = self.get_user_lesson_quiz(db, user_id, lesson_id, quiz_id)
            if not quiz:
                raise HTTPException(status_code=404, detail="Quiz not found")
            db.delete(quiz)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while deleting quiz"
            )
