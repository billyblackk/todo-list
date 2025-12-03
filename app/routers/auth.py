from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User as UserModel
from app.schemas.token import Token
from app.schemas.auth import TokenPair, TokenRefreshRequest


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenPair)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Log in with email + password.
    Returns an access token and a refresh token.
    - form_data.username -> email
    - form_data.password -> password
    """
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=TokenPair)
def refresh_tokens(
    payload: TokenRefreshRequest,
    db: Session = Depends(get_db),
):
    """
    Exchange a refresh token for a new access + refresh token pair.
    """
    decoded = decode_token(payload.refresh_token)

    # Ensure it's actually a refresh token
    token_type = decoded.get("type")
    if token_type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    email = decoded.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Issue a fresh token pair
    new_access = create_access_token(user.email)
    new_refresh = create_refresh_token(user.email)

    return TokenPair(
        access_token=new_access,
        refresh_token=new_refresh,
    )
