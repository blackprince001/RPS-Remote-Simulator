from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from schemas.user import AdminCreate
from rps_remote_simulator.database.models import User as UserModel
from utils.utils import get_db

admin = FastAPI()


@admin.get("/api/v1/users", tags=["admins"])
async def get_users(db: Session = Depends(get_db)) -> List[UserModel] | None:
    return db.scalars(select(UserModel)).all()


@admin.get("/api/v1/users/{user_id}", tags=["admins"])
async def get_user(user_id: int, db: Session = Depends(get_db)) -> UserModel:
    db_user = db.get(UserModel, user_id)

    if db_user.is_deleted is True:
        # handle this exception well too
        raise Exception("User not found!")
        
    return db_user


@admin.post("/api/v1/admins", tags=["admins"])
async def create_admin(
    new_admin: AdminCreate, db: Session = Depends(get_db)
) -> UserModel | None:
    db_admin = UserModel(**new_admin.dict())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


@admin.delete("/api/v1/users/{user_id}", tags=["admins"])
async def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    db_user = get_user(db, user_id)

    if db_user.is_deleted is True:
        # change this exception and handle it well with HTTPExceptions
        raise Exception("This user account has already been deleted!")
