from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import Question
from ..schemas.questions import QuestionCreate, QuestionUpdate
from ..schemas.user_progress import UserProgressCreate


class QuestionsRepository:
    def get_quiz_questions(self, db: Session, quiz_id: int) -> list[Question]:
        return db.query(Question).filter(Question.quiz_id == quiz_id).all()

    def get_question_by_id(self, db: Session, question_id: int) -> Question:
        question = (
            db.query(Question).filter(Question.question_id == question_id).first()
        )
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return question

    def create_question(
        self, db: Session, quiz_id: int, question_data: QuestionCreate
    ) -> Question:
        try:
            new_question = Question(
                quiz_id=quiz_id,
                question_text=question_data.question_text,
                question_type=question_data.question_type,
                options=question_data.options,
                correct_answer=question_data.correct_answer,
            )
            db.add(new_question)
            db.commit()
            db.refresh(new_question)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while creating question"
            )
        return new_question

    def update_question(
        self, db: Session, question_id: int, question_data: QuestionUpdate
    ) -> Question:
        try:
            question = self.get_question_by_id(db, question_id)
            for field, value in question_data.model_dump(exclude_unset=True).items():
                setattr(question, field, value)
            db.commit()
            db.refresh(question)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while updating question"
            )
        return question

    def delete_question(self, db: Session, question_id: int):
        try:
            question = self.get_question_by_id(db, question_id)
            db.delete(question)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while deleting question"
            )
