import asyncio
from sqlalchemy import text
from bot.database.session import engine, async_session
from bot.database.models import User

async def test_db():
    async with engine.begin() as conn:
        # 1. וידוא קיום טבלאות
        tables = await conn.run_sync(lambda c: [row[0] for row in c.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()])
        print("🗃️ Tables found:", tables)

        # 2. בדיקת עמודות בטבלת users
        cols = await conn.run_sync(lambda c: [row[1] for row in c.execute(text("PRAGMA table_info(users)")).fetchall()])
        print("👤 Users columns:", cols)

        # 3. הוספת משתמש דמה
        from sqlalchemy import insert
        stmt = insert(User).values(telegram_id=999999, language='he', role='user')
        await conn.execute(stmt)
        print("✅ User 999999 created")

        # 4. שליפת המשתמש
        result = await conn.execute(text("SELECT telegram_id, language FROM users WHERE telegram_id=999999"))
        user = result.fetchone()
        print("🔍 Retrieved user:", user)

        # 5. מחיקת דמה
        await conn.execute(text("DELETE FROM users WHERE telegram_id=999999"))
        print("🧹 Test user deleted")
        return True
    return False

async def main():
    success = await test_db()
    if success:
        print("\n✅ DB test passed!")
    else:
        print("\n❌ DB test failed")

asyncio.run(main())
