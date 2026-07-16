from typing import Optional

from pydantic import BaseModel, Field
from pydantic import model_validator


class UserOut(BaseModel):
    id: str
    username: str
    phone: Optional[str] = None
    isAdmin: bool


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=120)
    phone: str = Field(pattern=r"^1\d{10}$")
    password: str = Field(min_length=8, max_length=255)
    confirmPassword: str = Field(min_length=8, max_length=255)

    @model_validator(mode="after")
    def validate_password_rules(self):
        if self.password != self.confirmPassword:
            raise ValueError("Password confirmation does not match")
        if self.password == self.username:
            raise ValueError("Password must not equal username")
        if not any(ch.isalpha() for ch in self.password) or not any(ch.isdigit() for ch in self.password):
            raise ValueError("Password must include letters and digits")
        return self


class LoginRequest(BaseModel):
    account: str = Field(min_length=1, max_length=120)
    password: str = Field(min_length=1, max_length=255)


class LoginResponse(BaseModel):
    token: str
    user: UserOut
