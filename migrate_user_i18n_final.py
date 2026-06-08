import os
import sys

# === חשוב: הגדרת כל המשתנים לפני כל import של הבוט ===
os.environ.setdefault("BOT_TOKEN", "dummy_for_migration")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///bot.db")
# הוסף כאן כל משתנה נוסף שיש לך ב-.env אם יש

print("✅ Environment variables set for migration")

import asyncio
from sqlalchemy import text
from bot.database.session import async_session
from bot.database.models import User

async def migrate():
    print("🚀 Starting migration on Railway...")

    async with async_session() as session:
        # יצירת הטבלה אם לא קיימת
        await session.run_sync(lambda s: User.__table__.create(s.get_bind(), checkfirst=True))
        print("✅ Users table is ready")

        # הוספת עמודות
        columns = [
            ("language", "TEXT DEFAULT 'he'"),
            ("country",  "TEXT DEFAULT 'IL'"),
            ("timezone", "TEXT DEFAULT 'Asia/Jerusalem'"),
            ("currency", "TEXT DEFAULT 'ILS'")
        ]

        for col, definition in columns:
            try:
                await session.execute(text(f"""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS {col} {definition}
                """))
                print(f"✅ Column added/verified: {col}")
            except Exception as e:
                err = str(e).lower()
                if "duplicate column" in err or "already exists" in err:
                    print(f"⏭️ {col} already exists")
                else:
                    print(f"⚠️ Warning for {col}: {e}")

        await session.commit()
        print("🎉 Migration completed successfully on Railway!")

asyncio.run(migrate())
