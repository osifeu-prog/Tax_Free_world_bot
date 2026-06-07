# -*- coding: utf-8 -*-
import asyncio
from sqlalchemy import text
from bot.database.session import async_session

async def migrate():
    async with async_session() as session:
        # הוספת עמודות אם אינן קיימות (PostgreSQL)
        await session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(255) UNIQUE"))
        await session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS google_id VARCHAR(255) UNIQUE"))
        await session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255)"))
        await session.commit()
        print("Migration completed: columns added if missing")

asyncio.run(migrate())

