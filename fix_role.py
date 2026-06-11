import asyncio
from sqlalchemy import text
from bot.database.session import engine

async def fix():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'"))
            print("✅ role added")
        except Exception as e:
            print("role may already exist:", e)

asyncio.run(fix())
