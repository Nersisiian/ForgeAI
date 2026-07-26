from pydantic import EmailStr
from app.schemas.common import BaseSchema


class TokenResponse(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseSchema):
    email: EmailStr
    password: str


class RegisterRequest(BaseSchema):
    email: EmailStr
    password: str
    full_name: str | None = None


class RefreshRequest(BaseSchema):
    refresh_token: str