from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, select
from pydantic import BaseModel, EmailStr
import time
from app.core.config import settings
from app.auth.security import create_token, decode_token, verify_password, hash_password
from app.models.db import User

router = APIRouter(prefix="/auth", tags=["auth"])

engine = create_async_engine(settings.DB_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login(data: LoginIn, response: Response):
    async with async_session() as session:
        result = await session.exec(select(User).where(User.email == data.email))
        user = result.one_or_none()
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access = create_token(str(user.id), settings.ACCESS_TOKEN_EXPIRES_MIN*60)
        refresh = create_token(str(user.id), settings.REFRESH_TOKEN_EXPIRES_DAYS*24*3600)
        if settings.AUTH_COOKIES:
            response.set_cookie("access_token", access, httponly=True, secure=True, samesite="lax", max_age=settings.ACCESS_TOKEN_EXPIRES_MIN*60)
            response.set_cookie("refresh_token", refresh, httponly=True, secure=True, samesite="lax", max_age=settings.REFRESH_TOKEN_EXPIRES_DAYS*24*3600)
            return {"ok": True}
        return {"access_token": access, "refresh_token": refresh}

@router.post("/refresh")
async def refresh(response: Response, refresh_token: str | None = Cookie(default=None)):
    token = refresh_token
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    uid = payload["sub"]
    access = create_token(uid, settings.ACCESS_TOKEN_EXPIRES_MIN*60)
    if settings.AUTH_COOKIES:
        response.set_cookie("access_token", access, httponly=True, secure=True, samesite="lax", max_age=settings.ACCESS_TOKEN_EXPIRES_MIN*60)
        return {"ok": True}
    return {"access_token": access}

@router.post("/logout")
async def logout(response: Response):
    if settings.AUTH_COOKIES:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
    return {"ok": True}
