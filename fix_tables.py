import os
from sqlalchemy import text
from bot.database.session import engine
import asyncio

print("Current working directory:", os.getcwd())
print("bot.db full path:", os.path.abspath("bot.db"))
print("bot.db exists?", os.path.exists("bot.db"))

async def create_missing_tables():
    print("🔧 יוצר טבלאות...")
    try:
        async with engine.begin() as conn:
            # donations
            await conn.run_sync(lambda c: c.execute(text('''
                CREATE TABLE IF NOT EXISTS donations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')))
            # user_expenses
            await conn.run_sync(lambda c: c.execute(text('''
                CREATE TABLE IF NOT EXISTS user_expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL,
                    type TEXT,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')))
            print("✅ טבלאות נוצרו בהצלחה!")
    except Exception as e:
        print("❌ ERROR:", str(e))

asyncio.run(create_missing_tables())
print("סיום!")
