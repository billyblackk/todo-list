from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash, get_current_user

from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    hashed_password = get_password_hash(user_in.password)

    user = UserModel(
        email=user_in.email,
        hashed_password=hashed_password,
        is_active=True,
        role="user",
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/me", response_model=User)
def read_current_user(current_user: UserModel = Depends(get_current_user)):
    return current_user
