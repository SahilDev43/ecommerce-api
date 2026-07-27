from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.repositories import user_repository
from fastapi import  HTTPException
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token

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

def login(db: Session, login_data: UserLogin):

    user = user_repository.get_user_by_email(db, login_data.email)

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive"
        )

    access_token = create_access_token(data={"sub": str(user.id)})

    return Token(
        access_token=access_token,
        token_type="bearer"
    )