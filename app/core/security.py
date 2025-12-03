from datetime import datetime, timedelta, timezone
from typing import Optional, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User as UserModel
from app.core.config import settings

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

# For apps in production load these credentials from environment variables

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def _create_token(
    subject_email: str,
    expires_delta: timedelta,
    token_type: str,
) -> str:
    """
    Internal helper function to create a signed JWT.
    - Subject_email goes into the `sub` claim.
    - token_type is "access" or "refresh"
    """
    now = datetime.now(timezone.utc)

    payload: dict[str, Any] = {
        "sub": subject_email,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return encoded_jwt


def create_access_token(
    subject_email: str, expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates an access token for the given user email.
    """

    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    return _create_token(
        subject_email=subject_email, expires_delta=expires_delta, token_type="access"
    )


def create_refresh_token(subject_email: str) -> str:
    """
    Create a refresh token for the given user email.
    """
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    return _create_token(
        subject_email=subject_email, expires_delta=expires_delta, token_type="refresh"
    )


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode a JWT token and return the payload.
    Raises HTTPException(401) if invalid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not valdiate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    return payload


# ------------------------
# Current user dependency
# ------------------------


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserModel:
    """
    Decode the JWT, extract the user email, and load the user from the
    database.

    Raises a 401 if anything is wrong with the token or user.
    """
    payload = decode_token(token)

    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
