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
app.include_router(users_router, prefix="/me", tags=["users"])
app.include_router(courses_router, prefix="/me/courses", tags=["courses"])
app.include_router(
    modules_router, prefix="/me/courses/{course_id}/modules", tags=["modules"]
)
app.include_router(
    lessons_router,
    prefix="/me/courses/{course_id}/modules/{module_id}/lessons",
    tags=["lessons"],
)
app.include_router(
    quizzes_router,
    prefix="/me/courses/{course_id}/modules/{module_id}/lessons/{lesson_id}/quiz",
    tags=["quizzes"],
)
app.include_router(
    questions_router,
    prefix="/me/courses/{course_id}/modules/{module_id}/lessons/{lesson_id}/quiz/{quiz_id}/questions",
    tags=["questions"],
)

