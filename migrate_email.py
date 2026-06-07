import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:RITCyNjcMXJgHfbxDVLEhjdPBQDvFoGd@acela.proxy.rlwy.net:43231/railway").replace("postgresql://", "postgresql+asyncpg://")

async def run():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(255) UNIQUE"))
        await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR(255) UNIQUE"))
        await conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255)"))
    print("Migration done")
    await engine.dispose()

asyncio.run(run())
