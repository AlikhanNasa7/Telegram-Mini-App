from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.courses import router as courses_router
from app.api.modules import router as modules_router
from app.api.lessons import router as lessons_router
from app.api.quizzes import router as quizzes_router
from app.api.questions import router as questions_router
from app.api.user_progress import router as user_progress_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS middleware to allow all origins, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(courses_router, prefix="/courses", tags=["courses"])
app.include_router(modules_router, tags=["modules"])
app.include_router(lessons_router, tags=["lessons"])
app.include_router(quizzes_router, tags=["quizzes"])
app.include_router(questions_router, tags=["questions"])
