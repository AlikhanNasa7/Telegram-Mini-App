from pydantic import BaseModel
from typing import Optional


class ModuleCreate(BaseModel):
    title: str
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Introduction",
                "description": "Getting started with the course.",
            }
        }


class ModuleUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    position: Optional[int]


class ModuleOut(BaseModel):
    module_id: int
    course_id: int
    title: str
    description: Optional[str]
    position: Optional[int]

    class Config:
        orm_mode = True
