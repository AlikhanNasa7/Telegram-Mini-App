from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.courses import CoursesRepository
from ..schemas.courses import CourseCreate, CourseUpdate, CourseOut, Courses
from ..database.base import get_db
from ..llm import course_creator
from .modules import modules_repository
from .lessons import lessons_repository
from .quizzes import quizzes_repository
from .questions import questions_repository
import json


router = APIRouter()
courses_repository = CoursesRepository()


# Get all courses
@router.get("/", response_model=Courses)
def get_courses(
    db: Session = Depends(get_db),
    limit: int = 5,
    offset: int = 0,
):
    total_count, courses = courses_repository.get_courses(db, limit, offset)
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
def generate_course(
    user_id: int, learning_field: str, description: str, db: Session = Depends(get_db)
):
    if description.strip() == "":
        raise HTTPException(status_code=400, detail="Description cannot be empty")

    if learning_field.strip() == "":
        raise HTTPException(status_code=400, detail="Course name cannot be empty")

    try:
        # Generate course JSON
        # course_JSON = course_creator.create_course(learning_field, description)
        # course_data = json.loads(course_JSON)
        # print(course_data)

        course_data = {
            "title": "Python Programming Basics",
            "description": "An introductory course on programming, focusing on fundamental concepts for beginners.",
            "modules": [
                {
                    "title": "Module 1: Getting Started with Python",
                    "description": "Learn the basics of Python programming, including syntax, variables, and basic operations.",
                    "position": 1,
                    "lessons": [
                        {
                            "title": "Lesson 1: Introduction to Python",
                            "content": [
                                {
                                    "type": "text",
                                    "value": "Python is a high-level, interpreted programming language known for its easy-to-read syntax and versatility. It is a great first language to learn as its syntax is clear and concise. Python can be used for web development, data analysis, automation, and more. In this lesson, you will learn about Python syntax, how to set up Python on your computer, and how to write your first Python program.",
                                },
                                {
                                    "type": "text",
                                    "value": "You'll start by downloading Python from the official Python website and installing it on your computer. Once installed, you can use the command line or an Integrated Development Environment (IDE) like PyCharm or Jupyter Notebook to write and execute your Python code. Writing your first 'Hello, World!' program is a good point of entry into Python programming. This simple program illustrates the process of writing a Python script and running it.",
                                },
                            ],
                            "position": 1,
                            "quizzes": [
                                {
                                    "title": "Quiz 1: Basics of Python",
                                    "description": "Test your understanding of Python basics and installation.",
                                    "position": 1,
                                    "questions": [
                                        {
                                            "question_text": "What is the command to write 'Hello, World!' in Python?",
                                            "question_type": "multiple_choice",
                                            "options": [
                                                "echo 'Hello, World!'",
                                                "print('Hello, World!')",
                                                "console.log('Hello, World!')",
                                            ],
                                            "correct_answer": "print('Hello, World!')",
                                        },
                                        {
                                            "question_text": "Is Python a high-level programming language?",
                                            "question_type": "true_false",
                                            "correct_answer": "true",
                                        },
                                    ],
                                },
                                {
                                    "title": "Quiz 2: Python Setup and Execution",
                                    "description": "Assess your knowledge on setting up Python and executing a simple program.",
                                    "position": 2,
                                    "questions": [
                                        {
                                            "question_text": "Which IDE can be used for Python programming?",
                                            "question_type": "multiple_choice",
                                            "options": [
                                                "Microsoft Word",
                                                "PyCharm",
                                                "Photoshop",
                                            ],
                                            "correct_answer": "PyCharm",
                                        },
                                        {
                                            "question_text": "Can Python scripts be executed from the command line?",
                                            "question_type": "true_false",
                                            "correct_answer": "true",
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "title": "Lesson 2: Variables and Basic Data Types",
                            "content": [
                                {
                                    "type": "text",
                                    "value": "Variables in Python are used to store information that can be referenced and manipulated. Python, being dynamically typed, does not require explicit declaration to reserve memory. The assignment operator is used to assign values to variables. Common data types include integers, float, string, and boolean. Understanding these basic data types and their operations is key to grasping more complex programming concepts.",
                                },
                                {
                                    "type": "text",
                                    "value": "Integers and floats are used to represent whole and decimal numbers respectively, whereas strings represent sequences of characters. Booleans are True or False values used in logical expressions. Throughout this lesson, examples will illustrate how to declare variables, output their values, and perform basic operations with them.",
                                },
                            ],
                            "position": 2,
                            "quizzes": [
                                {
                                    "title": "Quiz 1: Understanding Variables",
                                    "description": "Test your understanding of variables and data types in Python.",
                                    "position": 1,
                                    "questions": [
                                        {
                                            "question_text": "Which of the following is a valid variable name in Python?",
                                            "question_type": "multiple_choice",
                                            "options": [
                                                "1variable",
                                                "variable1",
                                                "variable-1",
                                            ],
                                            "correct_answer": "variable1",
                                        },
                                        {
                                            "question_text": "In Python, you can assign a string to a variable without declaring its type.",
                                            "question_type": "true_false",
                                            "correct_answer": "true",
                                        },
                                    ],
                                },
                                {
                                    "title": "Quiz 2: Data Types and Operations",
                                    "description": "Evaluate your skills in using basic data types and performing simple operations.",
                                    "position": 2,
                                    "questions": [
                                        {
                                            "question_text": "What type is the result of 5 + 3.2 in Python?",
                                            "question_type": "multiple_choice",
                                            "options": ["int", "float", "str"],
                                            "correct_answer": "float",
                                        },
                                        {
                                            "question_text": "In Python, 'True' and 'False' are examples of Boolean values.",
                                            "question_type": "true_false",
                                            "correct_answer": "true",
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
                {
                    "title": "Module 2: Control Structures",
                    "description": "Understand how to control the flow of your program using if statements, loops, and functions.",
                    "position": 2,
                    "lessons": [
                        {
                            "title": "Lesson 1: Conditional Statements",
                            "content": [
                                {
                                    "type": "text",
                                    "value": "Conditional statements, like 'if', allow your program to make decisions. These statements evaluate expressions and, based on whether the expression is true or false, execute certain blocks of code. This lesson will cover the syntax of using if, else if (elif in Python), and else statements, and how to apply them effectively to control the flow of your program.",
                                },
                                {
                                    "type": "text",
                                    "value": "The if statement evaluates a boolean expression; if true, the block under the if statement is executed. Else if (elif) is checked if the previous condition is false, allowing you to test multiple expressions. Else executes if no previous conditions are true, providing a default case. Incorporate conditional logic to create dynamic and responsive programs.",
                                },
                            ],
                            "position": 1,
                            "quizzes": [
                                {
                                    "title": "Quiz 1: Understanding If Statements",
                                    "description": "Assess your understanding of conditional logic in Python.",
                                    "position": 1,
                                    "questions": [
                                        {
                                            "question_text": "What will be the output of if (5 > 3) print('Hello')?",
                                            "question_type": "multiple_choice",
                                            "options": ["Hello", "Nothing", "Error"],
                                            "correct_answer": "Hello",
                                        },
                                        {
                                            "question_text": "The 'else' statement can be used after an 'if' statement.",
                                            "question_type": "true_false",
                                            "correct_answer": "true",
                                        },
                                    ],
                                },
                                {
                                    "title": "Quiz 2: Chaining Conditions with Elif",
                                    "description": "Test your knowledge on using 'elif' for multiple conditions.",
                                    "position": 2,
                                    "questions": [
                                        {
                                            "question_text": "Which statement checks multiple conditions in Python?",
                                            "question_type": "multiple_choice",
                                            "options": ["if", "elif", "else"],
                                            "correct_answer": "elif",
                                        },
                                        {
                                            "question_text": "Python allows you to use multiple 'elif' statements sequentially.",
                                            "question_type": "true_false",
                                            "correct_answer": "true",
                                        },
                                    ],
                                },
                            ],
                        },
                        {
                            "title": "Lesson 2: Loops and Iteration",
                            "content": [
                                {
                                    "type": "text",
                                    "value": "Loops are fundamental to executing repetitive tasks efficiently. Python offers for and while loops to iterate over data structures or repeat operations until a condition is met. This lesson explores how to use loops effectively, writing syntactically correct loop structures to perform tasks like iterating over lists or only executing sections of code when certain conditions are met.",
                                },
                                {
                                    "type": "text",
                                    "value": "The 'for' loop iterates over elements of a list, set, dictionary, or any iterable. It is ideal for processing items when the number of iterations is predetermined. The 'while' loop executes while a condition is true and stops when the condition becomes false. By understanding and leveraging loops, you can write programs that are not only concise but also powerful in their ability to handle repetitive tasks.",
                                },
                            ],
                            "position": 2,
                            "quizzes": [
                                {
                                    "title": "Quiz 1: For Loops",
                                    "description": "Evaluate your comprehension of 'for' loops in Python.",
                                    "position": 1,
                                    "questions": [
                                        {
                                            "question_text": "Which loop would you use to iterate over a list of elements?",
                                            "question_type": "multiple_choice",
                                            "options": ["for", "while", "if"],
                                            "correct_answer": "for",
                                        },
                                        {
                                            "question_text": "A 'for' loop is suitable for iterating through elements when the data structure is known.",
                                            "question_type": "true_false",
                                            "correct_answer": "true",
                                        },
                                    ],
                                },
                                {
                                    "title": "Quiz 2: While Loops",
                                    "description": "Test your knowledge on using 'while' loops for conditional iteration.",
                                    "position": 2,
                                    "questions": [
                                        {
                                            "question_text": "Which loop keeps running as long as a condition is true?",
                                            "question_type": "multiple_choice",
                                            "options": ["for", "while", "if"],
                                            "correct_answer": "while",
                                        },
                                        {
                                            "question_text": "In a 'while' loop, an infinite loop occurs if the condition never becomes false.",
                                            "question_type": "true_false",
                                            "correct_answer": "true",
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        }
        # Create course from JSON
        create_course_from_json(course_data, db, user_id)

        return {"detail": "Course generated successfully"}

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="Failed to parse the generated course JSON."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


def create_course_from_json(json_data, db: Session, user_id: int):
    try:
        # Ensure the required keys are present
        if "title" not in json_data or "description" not in json_data:
            raise ValueError(
                "Course data is missing required fields: 'title' or 'description'"
            )

        # Create the course
        course_data = {
            "title": json_data.get("title", "Untitled Course"),
            "description": json_data.get("description", ""),
        }

        course_data = CourseCreate(
            title=course_data["title"], description=course_data["description"]
        )

        print(course_data)

        course = courses_repository.create_course(
            db=db, user_id=user_id, course_data=course_data
        )

        pass
        # Iterate over modules
        modules = json_data.get("modules", [])
        for module_data in modules:
            try:
                # Ensure module fields exist
                if not isinstance(module_data, dict):
                    raise ValueError("Module data should be a dictionary")

                if "title" not in module_data or "description" not in module_data:
                    raise ValueError(
                        "Module data is missing required fields: 'title' or 'description'"
                    )

                # Create module
                module_data_dict = {
                    "title": module_data["title"],
                    "description": module_data["description"],
                    "position": module_data.get("position", 1),
                }

                print(module_data_dict)
                module = modules_repository.create_module(
                    db=db, course_id=course.course_id, module_data=module_data_dict
                )

                # Iterate over lessons
                lessons = module_data.get("lessons", [])
                for lesson_data in lessons:
                    try:
                        # Ensure lesson fields exist
                        if not isinstance(lesson_data, dict):
                            raise ValueError("Lesson data should be a dictionary")

                        if "title" not in lesson_data or "content" not in lesson_data:
                            raise ValueError(
                                "Lesson data is missing required fields: 'title' or 'content'"
                            )

                        # Create lesson
                        lesson_data_dict = {
                            "title": lesson_data["title"],
                            "content": lesson_data["content"],
                            "position": lesson_data.get("position", 1),
                        }
                        print(lesson_data_dict)
                        lesson = lessons_repository.create_lesson(
                            db=db,
                            module_id=module.module_id,
                            lesson_data=lesson_data_dict,
                        )

                        # Iterate over quizzes
                        quizzes = lesson_data.get("quizzes", [])
                        for quiz_data in quizzes:
                            try:
                                # Ensure quiz fields exist
                                if not isinstance(quiz_data, dict):
                                    raise ValueError("Quiz data should be a dictionary")

                                if (
                                    "title" not in quiz_data
                                    or "description" not in quiz_data
                                ):
                                    raise ValueError(
                                        "Quiz data is missing required fields: 'title' or 'description'"
                                    )

                                # Create quiz
                                quiz_data_dict = {
                                    "title": quiz_data["title"],
                                    "description": quiz_data["description"],
                                    "position": quiz_data.get("position", 1),
                                }
                                quiz = quizzes_repository.create_quiz(
                                    db=db,
                                    lesson_id=lesson.lesson_id,
                                    quiz_data=quiz_data_dict,
                                )

                                # Iterate over questions
                                questions = quiz_data.get("questions", [])
                                for question_data in questions:
                                    try:
                                        # Ensure question fields exist
                                        if not isinstance(question_data, dict):
                                            raise ValueError(
                                                "Question data should be a dictionary"
                                            )

                                        if (
                                            "question_text" not in question_data
                                            or "question_type" not in question_data
                                        ):
                                            raise ValueError(
                                                "Question data is missing required fields: 'question_text' or 'question_type'"
                                            )

                                        # Create question
                                        question_data_dict = {
                                            "question_text": question_data[
                                                "question_text"
                                            ],
                                            "question_type": question_data[
                                                "question_type"
                                            ],
                                            "options": question_data.get("options"),
                                            "correct_answer": question_data.get(
                                                "correct_answer", ""
                                            ),
                                        }
                                        questions_repository.create_question(
                                            db=db,
                                            quiz_id=quiz.quiz_id,
                                            question_data=question_data_dict,
                                        )
                                    except Exception as e:
                                        db.rollback()
                                        raise HTTPException(
                                            status_code=500,
                                            detail=f"Failed to create question: {str(e)}",
                                        )
                            except Exception as e:
                                db.rollback()
                                raise HTTPException(
                                    status_code=500,
                                    detail=f"Failed to create quiz: {str(e)}",
                                )
                    except Exception as e:
                        db.rollback()
                        raise HTTPException(
                            status_code=500, detail=f"Failed to create lesson: {str(e)}"
                        )
            except Exception as e:
                db.rollback()
                raise HTTPException(
                    status_code=500, detail=f"Failed to create module: {str(e)}"
                )

        # Commit all changes
        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to create course: {str(e)}"
        )
