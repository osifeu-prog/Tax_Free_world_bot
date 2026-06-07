import asyncio, os, sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# קח DATABASE_URL כפרמטר, או מהסביבה
if len(sys.argv) > 1:
    DATABASE_URL = sys.argv[1]
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "")

if not DATABASE_URL:
    print("❌ יש להעביר DATABASE_URL כפרמטר: python check_railway_db.py 'postgresql://...'")
    sys.exit(1)

async def main():
    print(f"Connecting to: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.connect() as conn:
        tables = ["users", "user_profiles", "user_expenses", "command_logs", "referrals", "admins", "user_memory", "admin_requests", "households", "shopping_items", "chores"]
        for t in tables:
            try:
                result = await conn.execute(text(f"SELECT COUNT(*) FROM {t}"))
                count = result.scalar()
                print(f"  {t}: {count}")
            except Exception as e:
                print(f"  {t}: ❌ {e}")
        
        print("\n📊 Sample user_profiles:")
        try:
            result = await conn.execute(text("SELECT telegram_id, monthly_income FROM user_profiles LIMIT 3"))
            for row in result.fetchall():
                print(f"  ID: {row[0]}, Income: {row[1]}")
        except Exception as e:
            print(f"  Error: {e}")
        
        print("\n💰 Sample user_expenses:")
        try:
            result = await conn.execute(text("SELECT id, category, amount FROM user_expenses LIMIT 3"))
            for row in result.fetchall():
                print(f"  ID: {row[0]}, Category: {row[1]}, Amount: {row[2]}")
        except Exception as e:
            print(f"  Error: {e}")
    await engine.dispose()

asyncio.run(main())
