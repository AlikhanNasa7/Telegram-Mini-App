from .config import client


def create_course(thing_to_learn, description):
    prompt = (
        f"""
    You are an assistant that generates structured JSON responses for creating an educational course. The course structure will include the following hierarchy: Course -> Modules -> Lessons -> Quizzes -> Questions.

    Please generate a JSON response that represents a course related to the user description what he want to learn: "{thing_to_learn}", with the following description: "{description}". The course should be structured as follows:
    
    - The course should have 2 modules.
    - Each module should contain 2 lessons.
    - Each lesson should have 2 quizzes.
    - Each quiz should include 2 questions.

    The JSON should include the following fields:
    - Course:
        - `title`: The title of the course (summarize and generalize "{thing_to_learn}").
        - `description`: The description of the course (summarize and generalize "{description}").
        - `modules`: A list of modules.
    - Module:
        - `title`: The title of the module.
        - `description`: A brief description of the module.
        - `position`: The module's position (1-2).
        - `lessons`: A list of lessons.
    - Lesson:
        - `title`: The title of the lesson.
        - `content`: A brief overview of the lesson content.
        - `position`: The lesson's position within the module (1-2).
        - `quizzes`: A list of quizzes.
    - Quiz:
        - `title`: The title of the quiz.
        - `description`: A brief description of what the quiz covers.
        - `position`: The quiz's position within the lesson (1-2).
        - `questions`: A list of questions.
    - Question:
        - `question_text`: The text of the question.
        - `question_type`: The type of the question (either "multiple_choice" or "true_false").
        - `options`: If it is a multiple-choice question, provide a list of answer options.
        - `correct_answer`: The correct answer for the question.
    """
        + """
    Example JSON structure (simplified):
    {
        "title": "Course Title",
        "description": "Course Description",
        "modules": [
            {
                "title": "Module 1",
                "description": "Description of Module 1",
                "position": 1,
                "lessons": [
                    {
                        "title": "Lesson 1",
                        "content": "Content of Lesson 1",
                        "position": 1,
                        "image_url": "https://www.example.com/image1.jpg",
                        "content": [
                            {
                                "type": "text",
                                "value": "Text content here"
                            },
                            {
                                "type": "text",
                                "value": "Text content here"
                            }
                        ]
                        "quizzes": [
                            {
                                "title": "Quiz 1",
                                "description": "Description of Quiz 1",
                                "position": 1,
                                "questions": [
                                    {
                                        "question_text": "What is the capital of France?",
                                        "question_type": "multiple_choice",
                                        "options": ["Paris", "London", "Berlin", "Madrid"],
                                        "correct_answer": "Paris"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
    

    Please generate the full JSON response for the course with the specified structure, including appropriate titles, descriptions, and sample content for each level. Ensure the description field uses the provided description value. Do not include JSON tags in your response; provide a pure JSON response.
    """
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that provides JSON responses.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
