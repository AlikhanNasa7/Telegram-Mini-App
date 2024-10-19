from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import Course
from ..schemas.courses import CourseCreate, CourseUpdate, CourseOut
from .course_enrollment import CourseEnrollmentRepository


course_enrollment_repository = CourseEnrollmentRepository()


class CoursesRepository:
    def get_courses(self, db: Session, limit, offset):
        query = db.query(Course)
        total_count = query.count()
        db_courses = query.limit(limit).offset(offset).all()
        courses_out = [CourseOut.from_orm(course) for course in db_courses]
        return total_count, courses_out

    def get_all_courses(self, db: Session, user_id: int):
        query = db.query(Course)
        total_count = query.count()
        db_courses = query.all()

        # Check enrollment status for each course
        courses_out = [
            CourseOut.from_orm(course).copy(
                update={
                    "is_enrolled": course_enrollment_repository.is_course_enrollment_exist(
                        user_id, course.course_id, db
                    )
                }
            )
            for course in db_courses
        ]

        return total_count, courses_out

    def get_course_by_id(self, db: Session, course_id: int, user_id: int) -> CourseOut:
        # Retrieve the course by its ID
        course = db.query(Course).filter(Course.course_id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        # Check if the user is enrolled in the course
        is_enrolled = course_enrollment_repository.is_course_enrollment_exist(
            user_id, course_id, db
        )

        # Create the CourseOut response model and include the is_enrolled field
        course_out = CourseOut.from_orm(course).copy(
            update={"is_enrolled": is_enrolled}
        )

        return course_out

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

    def enroll_to_course(self, user_id, course_id, db: Session):
        try:
            course_enrollment_repository.create_course_enrollment(
                user_id, course_id, db
            )
        except IntegrityError:
            raise HTTPException(
                status_code=400, detail="Integrity error while deleting course"
            )

    def disenroll_from_course(self, user_id, course_id, db: Session):
        try:
            course_enrollment_repository.delete_course_enrollment(
                user_id, course_id, db
            )
        except IntegrityError:
            raise HTTPException(
                status_code=400, detail="Integrity error while deleting course"
            )
