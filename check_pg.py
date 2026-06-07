import asyncio, os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL not set")
    exit(1)

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

async def main():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.connect() as conn:
        tables = ["users", "user_profiles", "user_expenses", "command_logs", "referrals"]
        for t in tables:
            try:
                result = await conn.execute(text(f"SELECT COUNT(*) FROM {t}"))
                print(f"  {t}: {result.scalar()}")
            except Exception as e:
                print(f"  {t}: ❌ {e}")
        print("\n📊 Sample user_expenses:")
        result = await conn.execute(text("SELECT category, amount FROM user_expenses LIMIT 5"))
        for row in result.fetchall():
            print(f"  {row[0]}: {row[1]}")
    await engine.dispose()

asyncio.run(main())
