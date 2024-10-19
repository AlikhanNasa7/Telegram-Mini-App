from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import CourseEnrollment
from ..schemas.course_enrollment import CourseEnrollmentCreate, CourseEnrollmentOut


class CourseEnrollmentRepository:
    def get_course_enrollments_of_user(self, user_id, db: Session):
        query = db.query(CourseEnrollment).filter(CourseEnrollment.user_id == user_id)
        total_count = query.count()
        db_course_enrollments_of_user = query.all()
        course_enrollments_out = [
            CourseEnrollmentOut.from_orm(course_enrollment)
            for course_enrollment in db_course_enrollments_of_user
        ]
        return total_count, course_enrollments_out

    def get_course_enrollments_of_course(self, course_id, db: Session):
        query = db.query(CourseEnrollment).filter(
            CourseEnrollment.course_id == course_id
        )
        total_count = query.count()
        db_course_enrollments_of_course = query.all()
        course_enrollments_out = [
            CourseEnrollmentOut.from_orm(course_enrollment)
            for course_enrollment in db_course_enrollments_of_course
        ]
        return total_count, course_enrollments_out

    def get_course_enrollment(self, user_id, course_id, db: Session):
        course_enrollment = (
            db.query(CourseEnrollment)
            .filter(
                CourseEnrollment.user_id == user_id,
                CourseEnrollment.course_id == course_id,
            )
            .first()
        )
        if not course_enrollment:
            raise HTTPException(status_code=404, detail="Course not found")
        return course_enrollment

    def is_course_enrollment_exist(self, user_id, course_id, db: Session) -> bool:
        course_enrollment = (
            db.query(CourseEnrollment)
            .filter(
                CourseEnrollment.user_id == user_id,
                CourseEnrollment.course_id == course_id,
            )
            .first()
        )
        return course_enrollment is not None

    def create_course_enrollment(
        self, user_id, course_id, db: Session
    ) -> CourseEnrollment:
        try:
            existing_enrollment = (
                db.query(CourseEnrollment)
                .filter(
                    CourseEnrollment.user_id == user_id,
                    CourseEnrollment.course_id == course_id,
                )
                .first()
            )
            if existing_enrollment:
                raise HTTPException(
                    status_code=400, detail="You have already enrolled in the course"
                )
            new_course_enrollment = CourseEnrollment(
                user_id=user_id, course_id=course_id
            )
            db.add(new_course_enrollment)
            db.commit()
            db.refresh(new_course_enrollment)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while enrolling to course"
            )
        return new_course_enrollment

    def delete_course_enrollment(self, user_id, course_id, db: Session):
        try:
            course_enrollment = self.get_course_enrollment(user_id, course_id, db)
            db.delete(course_enrollment)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while disenrolling from course"
            )
