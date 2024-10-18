from .config import client


def create_course(thing_to_learn, description):
    prompt = f"""
        You are an assistant that generates structured JSON responses for creating an educational course. 
        The course should be focused on "{thing_to_learn}" with the following description: "{description}".
        The JSON structure should follow this hierarchy: Course -> Modules -> Lessons -> Quizzes -> Questions.
        
        Please create a JSON response that adheres to the following requirements:
        - The course should have 1 course object.
        - The course should include 2 modules.
        - Each module should contain 2 lessons.
        - Each lesson should have 2 quizzes.
        - Each quiz should contain 2 questions.

        The JSON response should have the following fields:
        - Course:
            - `title`: The title of the course (summarize "{thing_to_learn}").
            - `description`: A brief description of the course (summarize "{description}").
            - `modules`: A list of module objects.
        - Module:
            - `title`: The title of the module.
            - `description`: A brief description of the module.
            - `position`: The module's position within the course (1-2).
            - `lessons`: A list of lesson objects.
        - Lesson:
            - `title`: The title of the lesson.
            - `content`: A list of content objects (e.g., text, images, videos). (You use text only). You need to include text that will teach student and then ask his knowledge with quizzes. You can write a lot here, this is kind of wikipedia article. 2-4 big paragraphs. Make it as useful as possible.
            - `position`: The lesson's position within the module (1-2).
            - `quizzes`: A list of quiz objects.
        - Quiz:
            - `title`: The title of the quiz.
            - `description`: A brief description of the quiz content.
            - `position`: The quiz's position within the lesson (1-2).
            - `questions`: A list of question objects.
        - Question:
            - `question_text`: The text of the question.
            - `question_type`: The type of the question, either "multiple_choice" or "true_false".
            - `options`: If it is a multiple-choice question, provide a list of options.
            - `correct_answer`: The correct answer for the question.

        Example JSON structure (simplified):

        {{
            "title": "Title of the Course",
            "description": "Description of the Course",
            "modules": [
                {{
                    "title": "Module 1",
                    "description": "Description of Module 1",
                    "position": 1,
                    "lessons": [
                        {{
                            "title": "Lesson 1",
                            "content": [
                                {{"type": "text", "value": "Lesson 1 Content"}},
                                {{"type": "text", "value": "Lesson 1 Content"}}    
                            ],
                            "position": 1,
                            "quizzes": [
                                {{
                                    "title": "Quiz 1",
                                    "description": "Quiz 1 Description",
                                    "position": 1,
                                    "questions": [
                                        {{
                                            "question_text": "What is the capital of France?",
                                            "question_type": "multiple_choice",
                                            "options": ["Paris", "London", "Berlin", "Madrid"],
                                            "correct_answer": "Paris"
                                        }},
                                        {{
                                            "question_text": "Is the Earth round?",
                                            "question_type": "true_false",
                                            "correct_answer": "true"
                                        }}
                                    ]
                                }}
                            ]
                        }}
                    ]
                }}
            ]
        }}

        Please generate a fully detailed JSON response according to the given specifications. Only return the JSON response. Do not include any additional text. Do not include any tags like json before JSON itself PURE JSON.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that provides JSON responses.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
