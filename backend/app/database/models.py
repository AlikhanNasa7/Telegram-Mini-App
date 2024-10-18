from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Text,
    DateTime,
    Enum,
    JSON,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)  # Telegram user ID
    username = Column(String(50), unique=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
    tokens_balance = Column(Integer, default=0)
    experience_points = Column(Integer, default=0)
    level = Column(Integer, default=1)

    courses = relationship("Course", back_populates="user")
    progress_records = relationship("UserProgress", back_populates="user")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}')>"


class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))  # New foreign key
    title = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="courses")
    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course(course_id={self.course_id}, title='{self.title}')>"


class Module(Base):
    __tablename__ = 'modules'

    module_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    title = Column(String(100), nullable=False)
    description = Column(Text)
    position = Column(Integer)

    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Module(module_id={self.module_id}, title='{self.title}', position={self.position})>"


class Lesson(Base):
    __tablename__ = 'lessons'

    lesson_id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey('modules.module_id'))
    title = Column(String(100), nullable=False)
    content = Column(Text)
    position = Column(Integer)

    module = relationship("Module", back_populates="lessons")
    quizzes = relationship("Quiz", back_populates="lesson", cascade="all, delete-orphan")
    progress_records = relationship("UserProgress", back_populates="lesson")

    def __repr__(self):
        return f"<Lesson(lesson_id={self.lesson_id}, title='{self.title}', position={self.position})>"


class Quiz(Base):
    __tablename__ = 'quizzes'

    quiz_id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'))
    title = Column(String(100), nullable=False)
    description = Column(Text)
    position = Column(Integer)

    lesson = relationship("Lesson", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    progress_records = relationship("UserProgress", back_populates="quiz")

    def __repr__(self):
        return f"<Quiz(quiz_id={self.quiz_id}, title='{self.title}', position={self.position})>"


class Question(Base):
    __tablename__ = 'questions'

    question_id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'))
    question_text = Column(Text, nullable=False)
    question_type = Column(
        Enum('multiple_choice', 'true_false', name='question_types'), nullable=False
    )
    options = Column(JSON)  # Available options for multiple-choice
    correct_answer = Column(String(255))  # Correct answer(s)

    quiz = relationship("Quiz", back_populates="questions")

    def __repr__(self):
        return f"<Question(question_id={self.question_id}, question_type='{self.question_type}')>"


class UserProgress(Base):
    __tablename__ = 'user_progress'

    progress_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'), nullable=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.quiz_id'), nullable=True)
    status = Column(
        Enum('not_started', 'in_progress', 'completed', name='progress_status'), nullable=False
    )
    score = Column(Float)
    last_accessed = Column(DateTime, default=datetime.utcnow)
    attempts = Column(Integer, default=0)

    user = relationship("User", back_populates="progress_records")
    lesson = relationship("Lesson", back_populates="progress_records")
    quiz = relationship("Quiz", back_populates="progress_records")

    def __repr__(self):
        return f"<UserProgress(progress_id={self.progress_id}, user_id={self.user_id}, status='{self.status}')>"