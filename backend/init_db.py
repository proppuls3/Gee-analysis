import asyncio
from backend.database.session import engine
from backend.database.models import Base

async def init_db():
    async with engine.begin() as conn:
        print("Dropping old tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("Creating new tables...")
        await conn.run_sync(Base.metadata.create_all)
    print("Database schema successfully recreated.")

if __name__ == "__main__":
    asyncio.run(init_db())
