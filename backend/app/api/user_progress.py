from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.user_progress import UserProgressRepository
from ..schemas.user_progress import UserProgressCreate
from ..database.base import get_db

router = APIRouter()
