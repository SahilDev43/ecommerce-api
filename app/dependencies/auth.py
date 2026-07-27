from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import ALGORITHM, SECRET_KEY
from jose import jwt, JWTError
from app.repositories import user_repository
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/login"
)

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )

        user = user_repository.get_user_by_id(db, int(user_id))

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    return user

def require_admin(
        current_user: User = Depends(get_current_user) 
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to this"
        )

    return current_user