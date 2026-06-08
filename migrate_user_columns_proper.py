import asyncio
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import text

async def migrate_user_columns():
    async with async_session() as session:
        # יצירת הטבלה אם לא קיימת
        await session.run_sync(lambda s: User.__table__.create(s.get_bind(), checkfirst=True))
        print("✅ טבלת users מוכנה")

        # הוספת עמודות שפה בצורה בטוחה
        columns_to_add = [
            ("language", "TEXT DEFAULT 'he'"),
            ("country", "TEXT DEFAULT 'IL'"),
            ("timezone", "TEXT DEFAULT 'Asia/Jerusalem'"),
            ("currency", "TEXT DEFAULT 'ILS'")
        ]

        for col_name, definition in columns_to_add:
            try:
                await session.execute(text(f"""
                    ALTER TABLE users 
                    ADD COLUMN IF NOT EXISTS {col_name} {definition}
                """))
                print(f"✅ Added / verified column: {col_name}")
            except Exception as e:
                if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                    print(f"⏭️ {col_name} already exists")
                else:
                    print(f"⚠️ Error with {col_name}: {e}")

        await session.commit()
        print("🎉 Migration completed successfully on Railway!")

asyncio.run(migrate_user_columns())
