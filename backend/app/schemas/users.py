from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    user_id: int  # Telegram user ID

    class Config:
        schema_extra = {
            "example": {
                "user_id": 123456789,
            }
        }


class UserOut(BaseModel):
    user_id: int
    registration_date: datetime
    tokens_balance: int
    experience_points: int
    level: int

    class Config:
        orm_mode = True
