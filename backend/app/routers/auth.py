from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.auth import get_current_user
from ..core.db import get_db
from ..models import User
from ..schemas.auth import LoginRequest, LoginResponse, RegisterRequest, UserOut
from ..services.auth import (
    DuplicatePhoneError,
    DuplicateUsernameError,
    authenticate_user,
    create_access_token,
    create_user,
    serialize_user,
)

router = APIRouter()


@router.post("/api/auth/register", response_model=LoginResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = create_user(
            db,
            username=payload.username,
            phone=payload.phone,
            password=payload.password,
        )
    except DuplicateUsernameError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except DuplicatePhoneError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    return LoginResponse(
        token=create_access_token(user),
        user=serialize_user(user),
    )


@router.post("/api/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.account, payload.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return LoginResponse(
        token=create_access_token(user),
        user=serialize_user(user),
    )


@router.get("/api/auth/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return serialize_user(current_user)
