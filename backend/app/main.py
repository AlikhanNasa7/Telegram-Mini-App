from fastapi import FastAPI
from app.api.users import router as users_router
from app.api.courses import router as courses_router
from app.api.modules import router as modules_router
from app.api.lessons import router as lessons_router
from app.api.quizzes import router as quizzes_router
from app.api.questions import router as questions_router
from app.api.user_progress import router as user_progress_router

app = FastAPI()

# Include routers
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(courses_router, prefix="/courses", tags=["courses"])
app.include_router(modules_router, prefix="/", tags=["modules"])
app.include_router(lessons_router, prefix="/", tags=["lessons"])
app.include_router(quizzes_router, prefix="/", tags=["quizzes"])
app.include_router(questions_router, prefix="/", tags=["questions"])
