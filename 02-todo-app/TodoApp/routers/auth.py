from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class MakeUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


def get_db():
    db = SessionLocal()
    try:
        yield db  # Makes db available to the calling function (e.g., a route handler).
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def get_user(db: db_dependency,
                   user_request: MakeUserRequest):
    user_model = Users(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=bcrypt_context.hash(user_request.password),
        role=user_request.role,
        is_active=True
    )
    db.add(user_model)
    db.commit()
