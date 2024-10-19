from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.lessons import LessonCreate
from app.schemas.modules import ModuleCreate
from app.schemas.questions import QuestionCreate
from app.schemas.quizzes import QuizCreate
from ..repositories.courses import CoursesRepository
from ..repositories.users import UsersRepository
from ..repositories.course_enrollment import CourseEnrollmentRepository
from ..schemas.courses import CourseCreate, CourseUpdate, CourseOut, Courses
from ..database.base import get_db, SessionLocal
from ..llm import course_creator
from .modules import modules_repository
from .lessons import lessons_repository
from .quizzes import quizzes_repository
from .questions import questions_repository
import json
from concurrent.futures import ThreadPoolExecutor
import asyncio
import logging


router = APIRouter()
courses_repository = CoursesRepository()
course_enrollment_repository = CourseEnrollmentRepository()
# Initialize a ThreadPoolExecutor with a suitable number of workers
executor = ThreadPoolExecutor(
    max_workers=4
)  # Adjust based on your server's capabilities

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


# # Get all courses
# @router.get("/", response_model=Courses)
# def get_courses(
#     db: Session = Depends(get_db),
#     limit: int = 5,
#     offset: int = 0,
# ):
#     total_count, courses = courses_repository.get_courses(db, limit, offset)
#     if not courses:
#         raise HTTPException(status_code=404, detail="No courses found")
#     return Courses(total=total_count, objects=courses)


# Get all courses
@router.get("/", response_model=Courses)
def get_courses(
    user_id: int,
    db: Session = Depends(get_db),
):
    total_count, courses = courses_repository.get_all_courses(db, user_id)
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found")
    return Courses(total=total_count, objects=courses)


# Get a specific course belonging to the user
@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = courses_repository.get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/{course_id}/enroll")
def enroll_to_course(course_id: int, user_id: int, db: Session = Depends(get_db)):
    courses_repository.enroll_to_course(user_id, course_id, db)
    return f"You have enrolled to the course with id: {course_id}"


@router.get("/{course_id}/disenroll")
def enroll_to_course(course_id: int, user_id: int, db: Session = Depends(get_db)):
    courses_repository.disenroll_from_course(user_id, course_id, db)
    return f"You have disenrolled from the course with id: {course_id}"


# Create a new course
@router.post("/", response_model=CourseOut)
def create_course(
    user_id: int, course_data: CourseCreate, db: Session = Depends(get_db)
):
    new_course = courses_repository.create_course(db, user_id, course_data)
    return new_course


# Update a course
@router.patch("/{course_id}", response_model=CourseOut)
def update_course(
    user_id: int,
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
):
    updated_course = courses_repository.update_course(
        db, user_id, course_id, course_data
    )
    return updated_course


# Delete a course
@router.delete("/{course_id}")
def delete_course(user_id: int, course_id: int, db: Session = Depends(get_db)):
    courses_repository.delete_course(db, user_id, course_id)
    return {"detail": "Course deleted successfully"}


@router.post("/generate")
async def generate_course(
    user_id: int, learning_field: str, description: str, db: Session = Depends(get_db)
):
    """
    Endpoint to generate a course based on the learning field and description.
    The course generation runs in the background to improve response time.
    """
    # Input Validation
    if not description.strip():
        raise HTTPException(status_code=400, detail="Description cannot be empty")

    if not learning_field.strip():
        raise HTTPException(status_code=400, detail="Learning field cannot be empty")

    # Schedule the background task
    loop = asyncio.get_event_loop()
    loop.run_in_executor(
        executor, create_course_background, user_id, learning_field, description
    )

    # Immediate response to the client
    return {"status": "processing"}


def create_course_background(user_id: int, learning_field: str, description: str):
    """
    Background task to generate a course, parse the JSON data, and populate the database.
    """
    # Create a new database session for the background thread
    db = SessionLocal()
    try:
        # Generate course JSON (Replace this with your actual LLM integration)
        course_JSON = course_creator.create_course(learning_field, description)
        course_data = json.loads(course_JSON)
        logger.info(f"Generated course data: {json.dumps(course_data, indent=4)}")

        # Create course from JSON
        create_course_from_json(course_data, db, user_id)

    except json.JSONDecodeError:
        logger.error("Failed to parse the generated course JSON.")
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error while creating course: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"An unexpected error occurred: {str(e)}")
    finally:
        db.close()


def create_course_from_json(json_data, db: Session, user_id: int):
    try:
        # Validate the input data using CourseCreate
        course_data = CourseCreate(
            title=json_data.get("title", "Untitled Course"),
            description=json_data.get("description", ""),
        )

        # Create the course in the database
        course = courses_repository.create_course(
            db=db, user_id=user_id, course_data=course_data
        )

        courses_repository.enroll_to_course(user_id, course.course_id, db)

        # Iterate over modules
        modules = json_data.get("modules", [])
        for module_data in modules:
            module_data_obj = ModuleCreate(
                title=module_data.get("title", "Untitled Module"),
                description=module_data.get("description", ""),
            )

            module = modules_repository.create_module(
                db=db, course_id=course.course_id, module_data=module_data_obj
            )
            # Iterate over lessons in the module
            lessons = module_data.get("lessons", [])
            for lesson_data in lessons:
                print(json.dumps(lesson_data, indent=4))
                lesson_data_obj = LessonCreate(
                    title=lesson_data.get("title", "Untitled Lesson"),
                    description=lesson_data.get("description", ""),
                    content=lesson_data.get("content", []),
                )

                lesson = lessons_repository.create_lesson(
                    db=db, module_id=module.module_id, lesson_data=lesson_data_obj
                )

                # Iterate over quizzes in the lesson
                quizzes = lesson_data.get("quizzes", [])
                for quiz_data in quizzes:
                    quiz_data_obj = QuizCreate(
                        title=quiz_data.get("title", "Untitled Quiz"),
                        description=quiz_data.get("description", ""),
                        position=quiz_data.get("position", 1),
                    )

                    quiz = quizzes_repository.create_quiz(
                        db=db, lesson_id=lesson.lesson_id, quiz_data=quiz_data_obj
                    )

                    # Iterate over questions in the quiz
                    questions = quiz_data.get("questions", [])
                    for question_data in questions:
                        question_data_obj = QuestionCreate(
                            question_text=question_data.get("question_text", ""),
                            question_type=question_data.get("question_type", ""),
                            options=question_data.get("options", []),
                            correct_answer=question_data.get("correct_answer", ""),
                        )

                        questions_repository.create_question(
                            db=db, quiz_id=quiz.quiz_id, question_data=question_data_obj
                        )

        # Commit all changes to the database
        db.commit()
        return {"detail": "Course created successfully"}

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Integrity error while creating course: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
