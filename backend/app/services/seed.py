import asyncio
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models.db import User
from app.services.users import get_user_by_email, create_user
from app.core.config import settings

async def seed():
    engine = create_async_engine(settings.DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        admin = await get_user_by_email(session, "admin@example.com")
        if settings.DEMO_SEED and not admin:
            await create_user(session, "admin@example.com", "changeme123", is_admin=True)

if __name__ == "__main__":
    asyncio.run(seed())
