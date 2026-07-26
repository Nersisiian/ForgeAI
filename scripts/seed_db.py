"""Seed database with sample data."""
import asyncio
from app.db.session import AsyncSessionLocal
from app.db.models.user import User
from app.core.security import get_password_hash

async def seed():
    async with AsyncSessionLocal() as session:
        admin = User(email="admin@example.com", hashed_password=get_password_hash("admin"), is_superuser=True)
        session.add(admin)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())