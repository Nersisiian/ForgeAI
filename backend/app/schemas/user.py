from uuid import UUID
from pydantic import EmailStr
from datetime import datetime
from app.schemas.common import BaseSchema


class UserResponse(BaseSchema):
    id: UUID
    email: EmailStr
    full_name: str | None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime | None


class UserUpdateRequest(BaseSchema):
    full_name: str | None = None
