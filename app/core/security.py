from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User as UserModel

# ----------------------------
# Password Hashing
# ----------------------------

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# Used when creating a new user
def get_password_hash(password: str) -> str:
    if isinstance(password, bytes):
        password = password.decode("utf-8")
    return pwd_context.hash(password)


# Used when logging in
def verify_password(plain_password: str, hashed_password: str) -> bool:
    if isinstance(plain_password, bytes):
        plain_password = plain_password.decode("utf-8")
    return pwd_context.verify(plain_password, hashed_password)


# ----------------------------
# JWT setting & helper
# ----------------------------

# For real apps load these credentials from environment variables

SECRET_KEY = "change-me-in-production-very-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a signed JWT token containing the given data.
    Inputs passed in will typically be {"sub": user.email} or {"sub": str(user.id)}.
    """
    to_encode = data.copy()

    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Decode the JWT, extract the user email, and load the user from the
    database.

    Raises a 401 if anything is wrong with the token or user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        raise credentials_exception

    return user
