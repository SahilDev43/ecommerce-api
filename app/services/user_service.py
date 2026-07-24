from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories import user_repository
from fastapi import  HTTPException
from app.core.security import hash_password

def register_user(db: Session, user: UserCreate):

    existing_email = user_repository.get_user_by_email(db, user.email)

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    db_user = User(
    first_name=user.first_name,
    last_name=user.last_name,
    email=user.email,
    hashed_password=hashed_password
    )

    return user_repository.create_user(db, db_user)