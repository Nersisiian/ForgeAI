from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import BadRequestError, ForbiddenError, NotFoundError
from app.db.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def register(self, data: RegisterRequest) -> UserResponse:
        existing = (await self.session.execute(select(User).where(User.email == data.email))).scalar_one_or_none()
        if existing:
            raise BadRequestError("Email already registered")
        user = User(
            email=data.email,
            hashed_password=get_password_hash(data.password),
            full_name=data.full_name,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return UserResponse.model_validate(user)

    async def login(self, data: LoginRequest) -> TokenResponse:
        result = await self.session.execute(select(User).where(User.email == data.email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(data.password, user.hashed_password):
            raise ForbiddenError("Invalid credentials")
        if not user.is_active:
            raise ForbiddenError("User inactive")
        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})
        return TokenResponse(access_token=access, refresh_token=refresh)

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise ForbiddenError("Invalid refresh token")
        user_id = payload.get("sub")
        user = await self.session.get(User, user_id)
        if not user or not user.is_active:
            raise ForbiddenError("User not found or inactive")
        access = create_access_token({"sub": str(user.id)})
        new_refresh = create_refresh_token({"sub": str(user.id)})
        return TokenResponse(access_token=access, refresh_token=new_refresh)

    async def get_current_user(self, user_id: str) -> User:
        user = await self.session.get(User, user_id)
        if not user:
            raise NotFoundError("User not found")
        return user