import asyncio
from sqlalchemy import text
from bot.database.session import engine
import logging

logging.basicConfig(level=logging.INFO)

async def create_tables():
    try:
        async with engine.begin() as conn:
            # donations
            await conn.execute(text('''
                CREATE TABLE IF NOT EXISTS donations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            print("✅ donations table created")

            # user_expenses
            await conn.execute(text('''
                CREATE TABLE IF NOT EXISTS user_expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL,
                    type TEXT,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            print("✅ user_expenses table created")
        print("✅ All tables ready!")
    except Exception as e:
        print("❌ Error:", e)

asyncio.run(create_tables())
