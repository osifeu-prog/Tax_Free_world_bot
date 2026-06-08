import sqlite3
from bot.database.session import async_session
from bot.database.models import User
import asyncio

async def ensure_users_table():
    async with async_session() as session:
        # זה ייצור את הטבלה אם היא לא קיימת (SQLAlchemy)
        await session.run_sync(lambda s: User.__table__.create(s.get_bind(), checkfirst=True))
        print("✅ טבלת users מוכנה")
        
        # הוספת עמודות אם חסרות
        conn = sqlite3.connect('bot.db')  # fallback
        c = conn.cursor()
        existing = [i[1] for i in c.execute("PRAGMA table_info(users)").fetchall()]
        for col, definition in [
            ("language", "TEXT DEFAULT 'he'"),
            ("country", "TEXT DEFAULT 'IL'"),
            ("timezone", "TEXT DEFAULT 'Asia/Jerusalem'"),
            ("currency", "TEXT DEFAULT 'ILS'")
        ]:
            if col not in existing:
                c.execute(f"ALTER TABLE users ADD COLUMN {col} {definition}")
                print(f"✅ Added {col}")
        conn.commit()
        conn.close()

asyncio.run(ensure_users_table())
