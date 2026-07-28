from app.db.base import Base
from app.db.session import engine

async def initialize_database() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def close_database() -> None:
    await engine.dispose()
