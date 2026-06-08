import os
import asyncio
import sqlite3
from sqlalchemy import text
from bot.database.session import async_session
from bot.database.models import User

# העתקת משתני סביבה מ-Railway (בטוח)
os.environ.setdefault("BOT_TOKEN", "dummy_for_migration")  # רק כדי שה-Settings לא יקרוס

async def migrate_user_columns():
    print("🚀 Running migration on Railway...")

    async with async_session() as session:
        # יצירת טבלת users אם לא קיימת
        await session.run_sync(lambda s: User.__table__.create(s.get_bind(), checkfirst=True))
        print("✅ Table 'users' ready")

        # הוספת עמודות בצורה בטוחה
        columns = [
            ("language", "TEXT DEFAULT 'he'"),
            ("country",  "TEXT DEFAULT 'IL'"),
            ("timezone", "TEXT DEFAULT 'Asia/Jerusalem'"),
            ("currency", "TEXT DEFAULT 'ILS'")
        ]

        for col_name, definition in columns:
            try:
                await session.execute(text(f"""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS {col_name} {definition}
                """))
                print(f"✅ Column added/verified: {col_name}")
            except Exception as e:
                error_str = str(e).lower()
                if "duplicate column" in error_str or "already exists" in error_str:
                    print(f"⏭️ {col_name} already exists")
                else:
                    print(f"⚠️ Warning for {col_name}: {e}")

        await session.commit()
        print("🎉 Migration completed successfully!")

asyncio.run(migrate_user_columns())
