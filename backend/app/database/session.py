from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()


def _to_asyncpg_url(raw_url: str) -> str:
    """
    Convert a Neon connection string into a form asyncpg accepts.

    Neon connection strings include `sslmode` and `channel_binding` query
    params meant for libpq-based clients (psql, psycopg2). asyncpg does not
    recognize either as a DSN parameter and raises on connect, so we strip
    them here and pass SSL via `connect_args` on the engine instead. Also
    swaps the `postgresql://` scheme for the explicit `+asyncpg` driver.
    """
    parsed = urlparse(raw_url)
    query = parse_qs(parsed.query)
    query.pop("sslmode", None)
    query.pop("channel_binding", None)
    new_query = urlencode(query, doseq=True)
    return urlunparse(("postgresql+asyncpg", parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))


engine = create_async_engine(
    _to_asyncpg_url(settings.DATABASE_URL),
    pool_pre_ping=True,
    pool_size=3,
    max_overflow=2,
    connect_args={"ssl": "require"},
)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    """FastAPI dependency that yields a scoped async DB session per request."""
    async with AsyncSessionLocal() as session:
        yield session