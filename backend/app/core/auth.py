from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from ..core.db import get_db
from ..models import User
from ..services.auth import get_user_by_token
from ..services.storage_policy import is_admin_username


def get_current_user(
    authorization: str = Header(default=""),
    db: Session = Depends(get_db),
) -> User:
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_token(db, token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_auth(current_user: User = Depends(get_current_user)) -> str:
    return current_user.username


def require_admin(current_user: User = Depends(get_current_user)) -> str:
    if not (current_user.is_admin or is_admin_username(current_user.username)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user.username
