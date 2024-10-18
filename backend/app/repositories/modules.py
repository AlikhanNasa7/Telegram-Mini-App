from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ..database.models import Module
from ..schemas.modules import ModuleCreate, ModuleUpdate


class ModulesRepository:
    def get_user_course_modules(
        self, db: Session, user_id: int, course_id: int
    ) -> list[Module]:
        return db.query(Module).filter(Module.course_id == course_id).all()

    def get_user_course_module_by_id(
        self, db: Session, user_id: int, course_id: int, module_id: int
    ) -> Module:
        module = (
            db.query(Module)
            .filter(Module.course_id == course_id, Module.module_id == module_id)
            .first()
        )
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")
        return module

    def create_module(
        self, db: Session, user_id: int, course_id: int, module_data: ModuleCreate
    ) -> Module:
        try:
            # Query the number of existing modules in the course
            module_count = (
                db.query(Module).filter(Module.course_id == course_id).count()
            )

            # Set the position to be one more than the number of existing modules
            new_position = module_count + 1

            # Create the new module with the automatically calculated position
            new_module = Module(
                course_id=course_id,
                title=module_data.title,
                description=module_data.description,
                position=new_position,
            )
            db.add(new_module)
            db.commit()
            db.refresh(new_module)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while creating module"
            )
        return new_module

    def update_module(
        self,
        db: Session,
        user_id: int,
        course_id: int,
        module_id: int,
        module_data: ModuleUpdate,
    ) -> Module:
        try:
            module = self.get_user_course_module_by_id(
                db, user_id, course_id, module_id
            )
            for field, value in module_data.model_dump(exclude_unset=True).items():
                setattr(module, field, value)
            db.commit()
            db.refresh(module)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while updating module"
            )
        return module

    def delete_module(self, db: Session, user_id: int, course_id: int, module_id: int):
        try:
            module = self.get_user_course_module_by_id(
                db, user_id, course_id, module_id
            )
            db.delete(module)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Integrity error while deleting module"
            )
