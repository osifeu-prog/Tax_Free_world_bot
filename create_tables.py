import asyncio
from sqlalchemy import text
from bot.database.session import engine

async def create():
    async with engine.begin() as conn:
        # טבלת donations
        await conn.execute(text('''
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        '''))
        print("✅ donations table created")
        # טבלת user_expenses (למקרה שצריך)
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
asyncio.run(create())
