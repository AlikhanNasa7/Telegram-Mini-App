from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import Course
from ..schemas.courses import CourseCreate, CourseUpdate


class CoursesRepository:
    def get_courses(self, db: Session) -> list[Course]:
        return db.query(Course).all()

    def get_course_by_id(self, db: Session, course_id: int) -> Course:
        course = db.query(Course).filter(Course.course_id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course

    def create_course(
        self, db: Session, user_id: int, course_data: CourseCreate
    ) -> Course:
        try:
            new_course = Course(
                user_id=user_id,
                title=course_data.title,
                description=course_data.description,
            )
            db.add(new_course)
            db.commit()
            db.refresh(new_course)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while creating course"
            )
        return new_course

    def update_course(
        self, db: Session, user_id: int, course_id: int, course_data: CourseUpdate
    ) -> Course:
        try:
            course = self.get_course_by_id(db, course_id)
            if course.user_id != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="User is not authorized to update this course",
                )
            for field, value in course_data.model_dump(exclude_unset=True).items():
                setattr(course, field, value)
            db.commit()
            db.refresh(course)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while updating course"
            )
        return course

    def delete_course(self, db: Session, user_id: int, course_id: int):
        try:
            course = self.get_course_by_id(db, course_id)
            if course.user_id != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="User is not authorized to delete this course",
                )
            db.delete(course)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while deleting course"
            )
