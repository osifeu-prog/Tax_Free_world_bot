import asyncio
from bot.database.session import engine
from sqlalchemy import text

async def add_col():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN wallet_address VARCHAR(255)"))
            print("✅ wallet_address column added")
        except Exception as e:
            if "duplicate" in str(e).lower():
                print("Column already exists")
            else:
                print("Error:", e)

asyncio.run(add_col())
