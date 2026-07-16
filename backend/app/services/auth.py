from __future__ import annotations

import base64
import hashlib
import hmac
import json
import re
import secrets
import time
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..core.config import settings
from ..models import User

PHONE_PATTERN = re.compile(r"^1\d{10}$")


class AuthError(Exception):
    pass


class DuplicateUsernameError(AuthError):
    pass


class DuplicatePhoneError(AuthError):
    pass


@dataclass(frozen=True)
class TokenPayload:
    user_id: str
    exp: int


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000).hex()
    return f"{salt}${digest}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt, expected = password_hash.split("$", 1)
    except ValueError:
        return False
    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 200_000).hex()
    return hmac.compare_digest(actual, expected)


def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_PATTERN.fullmatch(phone))


def ensure_default_admin_user(db: Session) -> User:
    user = db.scalar(select(User).where(User.username == settings.auth_username))
    desired_hash = hash_password(settings.auth_password)
    desired_is_admin = settings.auth_username in settings.admin_users
    if user is None:
        user = User(
            username=settings.auth_username,
            phone=None,
            password_hash=desired_hash,
            is_admin=desired_is_admin,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    changed = False
    if not verify_password(settings.auth_password, user.password_hash):
        user.password_hash = desired_hash
        changed = True
    if user.is_admin != desired_is_admin:
        user.is_admin = desired_is_admin
        changed = True
    if changed:
        db.commit()
        db.refresh(user)
    return user


def bootstrap_auth_state(db: Session) -> None:
    ensure_default_admin_user(db)


def create_user(db: Session, *, username: str, phone: str, password: str) -> User:
    ensure_default_admin_user(db)
    existing_username = db.scalar(select(User).where(User.username == username))
    if existing_username is not None:
        raise DuplicateUsernameError("Username already exists")

    existing_phone = db.scalar(select(User).where(User.phone == phone))
    if existing_phone is not None:
        raise DuplicatePhoneError("Phone already exists")

    user = User(
        username=username,
        phone=phone,
        password_hash=hash_password(password),
        is_admin=username in settings.admin_users,
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as error:
        db.rollback()
        message = str(getattr(error, "orig", error)).lower()
        if "username" in message:
            raise DuplicateUsernameError("Username already exists") from error
        if "phone" in message:
            raise DuplicatePhoneError("Phone already exists") from error
        raise


def authenticate_user(db: Session, account: str, password: str) -> Optional[User]:
    ensure_default_admin_user(db)
    user = db.scalar(select(User).where(or_(User.username == account, User.phone == account)))
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(user: User) -> str:
    payload = json.dumps(
        {"sub": user.id, "exp": int(time.time()) + settings.auth_token_ttl_hours * 3600},
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    encoded_payload = base64.urlsafe_b64encode(payload).decode("utf-8").rstrip("=")
    signature = hmac.new(settings.auth_token.encode("utf-8"), encoded_payload.encode("utf-8"), hashlib.sha256).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")
    return f"hg.{encoded_payload}.{encoded_signature}"


def parse_access_token(token: str) -> Optional[TokenPayload]:
    try:
        prefix, encoded_payload, encoded_signature = token.split(".", 2)
    except ValueError:
        return None
    if prefix != "hg":
        return None
    expected_signature = hmac.new(
        settings.auth_token.encode("utf-8"),
        encoded_payload.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    actual_signature = _decode_base64url(encoded_signature)
    if actual_signature is None or not hmac.compare_digest(actual_signature, expected_signature):
        return None
    payload_raw = _decode_base64url(encoded_payload)
    if payload_raw is None:
        return None
    try:
        payload = json.loads(payload_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    user_id = payload.get("sub")
    expires_at = payload.get("exp")
    if not isinstance(user_id, str) or not user_id:
        return None
    if not isinstance(expires_at, int):
        return None
    if expires_at <= int(time.time()):
        return None
    return TokenPayload(user_id=user_id, exp=expires_at)


def get_user_by_token(db: Session, token: str) -> Optional[User]:
    if token == settings.auth_token:
        return ensure_default_admin_user(db)
    payload = parse_access_token(token)
    if payload is None:
        return None
    return db.get(User, payload.user_id)


def serialize_user(user: User) -> dict[str, object]:
    return {
        "id": user.id,
        "username": user.username,
        "phone": user.phone,
        "isAdmin": user.is_admin or user.username in settings.admin_users,
    }


def _decode_base64url(value: str) -> Optional[bytes]:
    padding = "=" * (-len(value) % 4)
    try:
        return base64.urlsafe_b64decode(value + padding)
    except (ValueError, TypeError):
        return None
