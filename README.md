# hackdetbot - AI-Powered Course Generator

bot link:
[https://t.me/hackdetbot]


backend documentation:
[https://telegram-mini-app-x496.onrender.com/docs]


# Backend


## 🚀 Overview

hackdetbot is an AI-powered platform for creating, managing, and enrolling in structured educational courses. It dynamically generates courses, modules, lessons, and quizzes based on user input, integrating AI-generated content, images, and text-to-speech (TTS) capabilities.

## 🌟 Features

### 🔐 User Authentication
- User registration and profile management.
- Token-based authentication for secure access.
- Enroll and track progress in courses.

### 📚 Course & Lesson Management
- AI-generated courses, including modules, lessons, and quizzes.
- Course enrollment and progress tracking.
- Auto-generated lesson images for enhanced visual learning.
- Text-to-speech (TTS) integration for audio lesson playback.

### 🧠 AI-Powered Generation
- Automatically generates structured courses using LLM.
- Retrieves relevant images using external APIs.
- Generates quizzes based on lesson content.

### 🎓 Quizzes & Progress Tracking
- Auto-generated quizzes with multiple-choice and true/false questions.
- Tracks user progress across courses and lessons.
- Rewards users with experience points and tokens for completing quizzes.

## 🛠️ Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Alembic
- **Database:** SQLite
- **AI Integration:** OpenAI (GPT), SerpAPI (Image retrieval)
- **TTS:** EdgeTTS for lesson audio generation
- **Async Processing:** ThreadPoolExecutor, asyncio
- **Authentication:** JWT
- **Infrastructure:** Docker, Render (Deployment)

## 📂 Project Structure
```
.
├── app
│   ├── alembic
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── de7386bba624_progress_2.py
│   ├── alembic.ini
│   ├── api
│   │   ├── courses.py
│   │   ├── lessons.py
│   │   ├── modules.py
│   │   ├── questions.py
│   │   ├── quizzes.py
│   │   ├── user_progress.py
│   │   └── users.py
│   ├── database
│   │   ├── base.py
│   │   └── models.py
│   ├── llm
│   │   ├── config.py
│   │   ├── course_creator.py
│   │   └── image_finder.py
│   ├── main.py
│   ├── repositories
│   │   ├── course_enrollment.py
│   │   ├── courses.py
│   │   ├── lessons.py
│   │   ├── modules.py
│   │   ├── questions.py
│   │   ├── quizzes.py
│   │   ├── user_progress.py
│   │   └── users.py
│   ├── schemas
│   │   ├── course_enrollment.py
│   │   ├── courses.py
│   │   ├── lessons.py
│   │   ├── modules.py
│   │   ├── questions.py
│   │   ├── quizzes.py
│   │   ├── user_progress.py
│   │   └── users.py
│   └── tts
│       └── tts.py
└── requirements.txt

10 directories, 36 files
```

## **Installation**

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/AlikhanNasa7/Telegram-Mini-App.git
    cd Telegram-Mini-App/backend
    ```

2. **Set up a Virtual Environment (optional but recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```


4. **Create .env File in the root directory and fill it with the following content**:
    ```
    OPENAI_API_KEY=your_openai_api_key
    SERPAPI_API_KEY=your_serpapi_key
    ```

5. **Initialize the Database**:
    ```bash
    alembic upgrade head
    ```

6. **Run the Application**:
    ```bash
    uvicorn app.main:app --reload
    ```

The API will now be accessible at http://127.0.0.1:8000 .
You may check endpoints at http://127.0.0.1:8000/docs .

## **API Endpoints**
### **🔐 User Authentication** ###
- POST /users/ - Register or retrieve a user
- GET /users/me - Get current user profile
- DELETE /users/ - Delete user account

### ** 📚 Courses ** ###
- POST /courses/ - Create a new course
- GET /courses/ - Get all courses
- GET /courses/{course_id} - Get a specific course
- GET /courses/{course_id}/enroll - Enroll in a course
- GET /courses/{course_id}/disenroll - Leave a course
- PATCH /courses/{course_id} - Update a course
- DELETE /courses/{course_id} - Delete a course

### ** 📖 Modules & Lessons ** ###
- POST /courses/{course_id}/modules/ - Add a module
- GET /courses/{course_id}/modules/ - List course modules
- POST /modules/{module_id}/lessons/ - Add a lesson
- GET /modules/{module_id}/lessons/ - List module lessons
- GET /lessons/{lesson_id}/audio - Get TTS audio for a lesson

### ** 🎓 Quizzes & Questions ** ###
- POST /lessons/{lesson_id}/quiz/ - Create a quiz
- GET /lessons/{lesson_id}/quiz/ - Get a quiz
- POST /quizzes/{quiz_id}/questions/ - Add a question
- GET /quizzes/{quiz_id}/questions/ - List quiz questions
- POST /lessons/{lesson_id}/quiz/submit - Submit quiz results


## Author ##
Backend Developed by Bekzhan Kimadiyev and Dinmukhamed Albek.
Fronted Developeb by Dastan Tynyshtyq and Alikhan Nashtay.
