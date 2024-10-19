from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, Response
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
from ..llm import image_finder
import random


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
        return Response(status_code=200, content="No courses found")
    return Courses(total=total_count, objects=courses)


# Get a specific course belonging to the user
@router.get("/{course_id}", response_model=CourseOut)
def get_course(course_id: int, user_id: int, db: Session = Depends(get_db)):
    course = courses_repository.get_course_by_id(db, course_id, user_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/{course_id}/enroll")
def enroll_to_course(course_id: int, user_id: int, db: Session = Depends(get_db)):
    courses_repository.enroll_to_course(user_id, course_id, db)
    return f"You have enrolled to the course with id: {course_id}"


@router.get("/{course_id}/disenroll")
def disenroll_to_course(course_id: int, user_id: int, db: Session = Depends(get_db)):
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
        # course_JSON = course_creator.create_course(learning_field, description)
        course_JSON = """{
    "title": "Trading Strategies",
    "description": "Learn to earn through smart trading.",
    "modules": [
        {
            "title": "Basics",
            "description": "Introduction to trading fundamentals.",
            "lessons": [
                {
                    "title": "Market Overview",
                    "description": "Understanding market dynamics",
                    "content": [
                        {
                            "type": "text",
                            "value": "The financial markets are vast networks where buyers and sellers trade assets like stocks, bonds, commodities, and currencies. Understanding market dynamics is crucial for any aspiring trader. The market is influenced by economic news, investor sentiment, and geopolitical events. Traders must keep abreast of these factors to make informed decisions. Successful trading involves analyzing market trends and making predictions about future movements."
                        },
                        {
                            "type": "text",
                            "value": "Markets can be divided into various categories, each with unique characteristics. The stock market involves shares of publicly traded companies, while the forex market deals with currencies. It's essential to recognize these differences to tailor your trading strategy effectively. Knowledge of market types and their behaviors forms the bedrock of a trader's understanding needed to navigate these waters."
                        }
                    ],
                    "quizzes": [
                        {
                            "title": "Market Dynamics",
                            "description": "Test your understanding of market basics.",
                            "questions": [
                                {
                                    "question_text": "What are some factors that influence market dynamics?",
                                    "question_type": "multiple_choice",
                                    "options": [
                                        "Economic news",
                                        "Investor sentiment",
                                        "Geopolitical events",
                                        "All of the above"
                                    ],
                                    "correct_answer": "All of the above"
                                },
                                {
                                    "question_text": "Is the stock market the same as the forex market?",
                                    "question_type": "true_false",
                                    "correct_answer": "false"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Trading Tools",
                    "description": "Introduction to essential trading tools",
                    "content": [
                        {
                            "type": "text",
                            "value": "A successful trader relies on various tools to analyze the markets and execute trades. Technical analysis tools, like charts and indicators, help predict future price movements based on past data. It's critical to familiarize yourself with candlestick patterns, moving averages, and momentum indicators to gauge market signals effectively."
                        },
                        {
                            "type": "text",
                            "value": "Fundamental analysis also plays an important role by considering economic data and company financials. Tools like economic calendars and company reports provide valuable insights into market conditions. By integrating both technical and fundamental analysis, traders can make more informed decisions and devise robust trading strategies."
                        }
                    ],
                    "quizzes": [
                        {
                            "title": "Tools Review",
                            "description": "Evaluate your knowledge of trading tools.",
                            "questions": [
                                {
                                    "question_text": "What type of analysis uses charts and indicators?",
                                    "question_type": "multiple_choice",
                                    "options": [
                                        "Technical analysis",
                                        "Fundamental analysis",
                                        "Qualitative analysis",
                                        "Quantitative analysis"
                                    ],
                                    "correct_answer": "Technical analysis"
                                },
                                {
                                    "question_text": "Fundamental analysis focuses on economic data and company financials.",
                                    "question_type": "true_false",
                                    "correct_answer": "true"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "title": "Advanced Techniques",
            "description": "Exploring sophisticated trading strategies.",
            "lessons": [
                {
                    "title": "Risk Management",
                    "description": "Effective strategies to manage trading risks",
                    "content": [
                        {
                            "type": "text",
                            "value": "Risk management is a critical component of successful trading. It involves setting predetermined stop-loss orders to limit potential losses and diversifying the trading portfolio to spread risk. Good risk management practices ensure that no single trade or asset disproportionately affects the trader's overall portfolio."
                        },
                        {
                            "type": "text",
                            "value": "It's also essential to determine an appropriate risk-reward ratio for each trade. This involves assessing potential losses against expected gains to decide whether a trade is worth pursuing. A sound understanding of risk management helps traders protect their capital and sustain long-term success."
                        }
                    ],
                    "quizzes": [
                        {
                            "title": "Risk Practice",
                            "description": "Assess your risk management understanding.",
                            "questions": [
                                {
                                    "question_text": "What is a key strategy in risk management?",
                                    "question_type": "multiple_choice",
                                    "options": [
                                        "Stop-loss orders",
                                        "Ignoring losses",
                                        "Single trade focus",
                                        "Random entries"
                                    ],
                                    "correct_answer": "Stop-loss orders"
                                },
                                {
                                    "question_text": "Diversifying the portfolio reduces trading risk.",
                                    "question_type": "true_false",
                                    "correct_answer": "true"
                                }
                            ]
                        }
                    ]
                },
                {
                    "title": "Trading Psychology",
                    "description": "Mastering mental aspects of trading",
                    "content": [
                        {
                            "type": "text",
                            "value": "Trading psychology is about managing emotions and maintaining a disciplined mindset during trading. Emotions like greed and fear can lead to poor decision-making, resulting in losses. Traders must develop strategies to cope with stress and remain focused on their trading plans."
                        },
                        {
                            "type": "text",
                            "value": "Maintaining emotional equilibrium involves setting realistic expectations and adhering to a predefined trading strategy. Regularly reviewing and adjusting trading plans can also help traders stay on track. Achieving a balanced state of mind enables traders to stick to their strategies and make rational trading decisions."
                        }
                    ],
                    "quizzes": [
                        {
                            "title": "Mental Edge",
                            "description": "Verify your understanding of trading psychology.",
                            "questions": [
                                {
                                    "question_text": "Which emotion can negatively impact trading decisions?",
                                    "question_type": "multiple_choice",
                                    "options": [
                                        "Greed",
                                        "Fear",
                                        "Both",
                                        "None"
                                    ],
                                    "correct_answer": "Both"
                                },
                                {
                                    "question_text": "A balanced mindset is crucial for sticking to a trading strategy.",
                                    "question_type": "true_false",
                                    "correct_answer": "true"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}
"""
        course_data = json.loads(course_JSON)
        logger.info(f"Generated course data: {json.dumps(course_data, indent=4)}")

        # print(json.dumps(course_data, indent=4))
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
        # print(json.dumps(json_data, indent=4))
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

                content_dict = lesson_data.get("content", [])

                images = image_finder.get_images(course.title)
                random.shuffle(images)
                lesson_data["image_url"] = images[0]["image"]
                for i in range(3):
                    image_data = images[i]

                    content_dict.append(
                        {
                            "type": "image",
                            "value": image_data["image"],
                            "description": image_data["title"],
                        }
                    )

                random.shuffle(content_dict)

                lesson_data_obj = LessonCreate(
                    title=lesson_data.get("title", "Untitled Lesson"),
                    description=lesson_data.get("description", ""),
                    content=content_dict,
                    image_url=lesson_data.get("image_url", ""),
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
