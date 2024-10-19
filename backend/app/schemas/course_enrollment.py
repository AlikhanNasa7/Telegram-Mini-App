from pydantic import BaseModel


class CourseEnrollmentCreate(BaseModel):
    user_id: int
    course_id: int


class CourseEnrollmentOut(BaseModel):
    user_id: int
    course_id: int


class CourseEnrollmentDelete(BaseModel):
    user_id: int
    course_id: int
