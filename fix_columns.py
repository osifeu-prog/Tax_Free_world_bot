import asyncio
from sqlalchemy import text
from bot.database.session import engine

async def fix():
    async with engine.begin() as conn:
        # הוסף role אם חסר
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'"))
            print("✅ column 'role' added")
        except Exception as e:
            print("role column maybe exists:", e)
        # הוסף wallet_address אם חסר
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN wallet_address VARCHAR(255)"))
            print("✅ column 'wallet_address' added")
        except Exception as e:
            print("wallet_address maybe exists:", e)
        # הוסף points אם חסר
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN points FLOAT DEFAULT 0"))
            print("✅ column 'points' added")
        except Exception as e:
            print("points maybe exists:", e)
        # הוסף last_gift_date אם חסר
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN last_gift_date VARCHAR(50)"))
            print("✅ column 'last_gift_date' added")
        except Exception as e:
            print("last_gift_date maybe exists:", e)
        # הוסף gift_shares_today
        try:
            await conn.execute(text("ALTER TABLE users ADD COLUMN gift_shares_today INTEGER DEFAULT 0"))
            print("✅ column 'gift_shares_today' added")
        except Exception as e:
            print("gift_shares_today maybe exists:", e)

asyncio.run(fix())
print("✅ כל העמודות החסרות טופלו")
