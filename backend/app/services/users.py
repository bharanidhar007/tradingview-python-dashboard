from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.db import User
from app.auth.security import hash_password, verify_password

async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    result = await session.exec(select(User).where(User.email == email))
    return result.one_or_none()

async def create_user(session: AsyncSession, email: str, password: str, is_admin: bool = False) -> User:
    u = User(email=email, hashed_password=hash_password(password), is_admin=is_admin)
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u
