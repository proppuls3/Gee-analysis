import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from backend.database.models import Base

# Use Google Cloud SQL (PostgreSQL) if DATABASE_URL is set, otherwise default to local SQLite.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./gee_leads.db")

engine = create_async_engine(DATABASE_URL, echo=False)

# Create an async session factory
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    """
    Creates all tables based on the models.py schema.
    In a true production environment, we use Alembic for this.
    """
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """
    Dependency injection for FastAPI routes or standalone scripts.
    """
    async with AsyncSessionLocal() as session:
        yield session
