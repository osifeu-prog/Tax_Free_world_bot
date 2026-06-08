from bot.database.session import engine
from sqlalchemy import text
import asyncio

async def add_lang_columns():
    """ מוסיף עמודות שפה לטבלת users אם לא קיימות """
    async with engine.begin() as conn:
        result = await conn.execute(text("PRAGMA table_info(users)"))
        existing = [row[1] for row in result.fetchall()]
        columns = {
            "language": "TEXT DEFAULT 'he'",
            "country": "TEXT DEFAULT 'IL'",
            "timezone": "TEXT DEFAULT 'Asia/Jerusalem'",
            "currency": "TEXT DEFAULT 'ILS'"
        }
        for col, definition in columns.items():
            if col not in existing:
                await conn.execute(text(f"ALTER TABLE users ADD COLUMN {col} {definition}"))
                print(f"✅ Added column {col}")
