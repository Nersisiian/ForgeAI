from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db, get_current_active_user
from app.db.models.user import User
from app.schemas.user import UserResponse, UserUpdateRequest

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_active_user)):
return UserResponse.model_validate(current_user)

@router.put("/me", response_model=UserResponse)
async def update_current_user(
data: UserUpdateRequest,
db: AsyncSession = Depends(get_db),
current_user: User = Depends(get_current_active_user),
):
if data.full_name is not None:
current_user.full_name = data.full_name
await db.commit()
await db.refresh(current_user)
return UserResponse.model_validate(current_user)
