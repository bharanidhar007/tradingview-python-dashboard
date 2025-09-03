from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings, ALLOWED_ORIGINS
from app.api.auth import router as auth_router
from app.api.private import router as private_router
from app.tv.udf import router as tv_udf_router
from app.services.seed import seed

app = FastAPI(title="Private Trading Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_start():
    await seed()

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(auth_router)
app.include_router(private_router, prefix="")
app.include_router(tv_udf_router)
