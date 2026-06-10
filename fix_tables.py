from sqlalchemy import text
from bot.database.session import engine
import asyncio
import os

print("Current directory:", os.getcwd())

async def create_missing_tables():
    print("🔧 מנסה ליצור טבלאות...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda c: c.execute(text('''
                CREATE TABLE IF NOT EXISTS donations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount REAL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')))
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
        print("❌ שגיאה:", e)

asyncio.run(create_missing_tables())
print("סיום!")
