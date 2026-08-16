from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.database import get_db

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
async def health_check() -> dict:
    """
    Lightweight liveness check.

    Intentionally does NOT touch the database. This endpoint is used as
    Render's health check target and, optionally, as an external keep-alive
    ping target to reduce free-tier cold starts — it must stay fast and
    dependency-free.
    """
    return {"status": "ok"}


@app.get("/", tags=["system"])
async def root() -> dict:
    return {"service": settings.APP_NAME, "status": "running"}


@app.get("/health/db", tags=["system"])
async def health_check_db(db: AsyncSession = Depends(get_db)) -> dict:
    """
    Verifies live connectivity to Neon via the pooled connection.
    Separate from /health so the fast liveness check never depends on the
    database (Render's health check target must stay dependency-free).
    """
    await db.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
