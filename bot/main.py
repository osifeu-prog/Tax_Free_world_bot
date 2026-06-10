import asyncio
import logging
import os
from sqlalchemy import text
from aiogram import Bot, Dispatcher
from bot.database.session import engine
from bot.database.models import Base

# ייבוא הראוטרים שלך
from bot.routers.start import router as start_router
from bot.routers.profile import router as profile_router
from bot.routers.donate import router as donate_router
from bot.routers.pension import router as pension_router
from bot.routers.useless import router as useless_router
from bot.routers.admin import router as admin_router

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fix_missing_columns():
    """הוסף עמודות חסרות לטבלה users (role, wallet_address, points, etc)"""
    async with engine.begin() as conn:
        # בדיקת עמודות קיימות
        pragma = await conn.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in pragma.fetchall()]
        logger.info(f"Existing columns: {columns}")
        
        # הוסף role אם חסר
        if "role" not in columns:
            await conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'"))
            logger.info("✅ column 'role' added")
        # הוסף wallet_address
        if "wallet_address" not in columns:
            await conn.execute(text("ALTER TABLE users ADD COLUMN wallet_address VARCHAR(255)"))
            logger.info("✅ column 'wallet_address' added")
        # הוסף points
        if "points" not in columns:
            await conn.execute(text("ALTER TABLE users ADD COLUMN points FLOAT DEFAULT 0"))
            logger.info("✅ column 'points' added")
        # הוסף last_gift_date
        if "last_gift_date" not in columns:
            await conn.execute(text("ALTER TABLE users ADD COLUMN last_gift_date VARCHAR(50)"))
            logger.info("✅ column 'last_gift_date' added")
        # הוסף gift_shares_today
        if "gift_shares_today" not in columns:
            await conn.execute(text("ALTER TABLE users ADD COLUMN gift_shares_today INTEGER DEFAULT 0"))
            logger.info("✅ column 'gift_shares_today' added")

async def init_db():
    logger.info("🔧 Initializing database tables...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ All database tables initialized successfully!")
        await fix_missing_columns()
    except Exception as e:
        logger.error(f"❌ Failed to init tables: {e}")

async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(donate_router)
    dp.include_router(pension_router)
    dp.include_router(useless_router)
    dp.include_router(admin_router)
    
    logger.info("🚀 Bot starting polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
