from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr
    hashed_password: str
    is_admin: bool = False

class Signal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    timeframe: str
    timestamp: int  # ms
    kind: str       # e.g., 'buy' | 'sell' | 'exit'
    price: float
    meta: Optional[str] = None
