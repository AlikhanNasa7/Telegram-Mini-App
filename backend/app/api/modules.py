from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..repositories.modules import ModulesRepository
from ..schemas.modules import ModuleCreate, ModuleUpdate, ModuleOut
from ..database.base import get_db

router = APIRouter()
modules_repository = ModulesRepository()


# Get all modules within a specific course
@router.get("/", response_model=list[ModuleOut])
def get_course_modules(course_id: int, user_id: int, db: Session = Depends(get_db)):
    modules = modules_repository.get_user_course_modules(db, user_id, course_id)
    if not modules:
        raise HTTPException(status_code=404, detail="No modules found in this course")
    return modules


# Get a specific module within a course
@router.get("/{module_id}", response_model=ModuleOut)
def get_module(
    course_id: int, module_id: int, user_id: int, db: Session = Depends(get_db)
):
    module = modules_repository.get_user_course_module_by_id(
        db, user_id, course_id, module_id
    )
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


# Create a new module in a course
@router.post("/", response_model=ModuleOut)
def create_module(
    course_id: int,
    user_id: int,
    module_data: ModuleCreate,
    db: Session = Depends(get_db),
):
    new_module = modules_repository.create_module(db, user_id, course_id, module_data)
    return new_module


# Update a module
@router.patch("/{module_id}", response_model=ModuleOut)
def update_module(
    course_id: int,
    module_id: int,
    user_id: int,
    module_data: ModuleUpdate,
    db: Session = Depends(get_db),
):
    updated_module = modules_repository.update_module(
        db, user_id, course_id, module_id, module_data
    )
    return updated_module


# Delete a module
@router.delete("/{module_id}")
def delete_module(
    course_id: int, module_id: int, user_id: int, db: Session = Depends(get_db)
):
    modules_repository.delete_module(db, user_id, course_id, module_id)
    return {"detail": "Module deleted successfully"}
