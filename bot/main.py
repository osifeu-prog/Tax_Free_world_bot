import asyncio
import logging
import os
from sqlalchemy import text

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.database.session import engine
from bot.database.models import Base

# ====================== CORE ROUTERS ======================
from bot.routers.start import router as start_router
from bot.routers.profile import router as profile_router
from bot.routers.donate import router as donate_router
from bot.routers.pension import router as pension_router
from bot.routers.useless import router as useless_router
from bot.routers.admin import router as admin_router
from bot.routers.menu import router as menu_router
from bot.routers.budget import router as budget_router
from bot.routers.wallet import router as wallet_router
from bot.routers.welcome_onboarding import router as onboarding_router
from bot.routers.gamification import router as gamification_router
from bot.routers.webapp import router as webapp_router
from bot.routers.dashboard_simple import router as dashboard_simple_router

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not set")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fix_missing_columns():
    async with engine.begin() as conn:
        # טבלת users
        pragma = await conn.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in pragma.fetchall()]
        logger.info(f"Existing columns: {columns}")
        needed = {
            "role": "VARCHAR(20) DEFAULT 'user'",
            "wallet_address": "VARCHAR(255)",
            "points": "FLOAT DEFAULT 0",
            "xp": "INTEGER DEFAULT 0",
            "level": "INTEGER DEFAULT 1",
            "streak_days": "INTEGER DEFAULT 0",
            "last_active": "DATETIME",
            "achievements": "TEXT DEFAULT '[]'"
        }
        for col, definition in needed.items():
            if col not in columns:
                await conn.execute(text(f"ALTER TABLE users ADD COLUMN {col} {definition}"))
                logger.info(f"✅ Added {col}")
        # טבלת user_preferences (אם חסרים role/goal)
        pragma2 = await conn.execute(text("PRAGMA table_info(user_preferences)"))
        cols2 = [row[1] for row in pragma2.fetchall()]
        if "goal" not in cols2:
            await conn.execute(text("ALTER TABLE user_preferences ADD COLUMN goal VARCHAR(20)"))
            logger.info("✅ Added goal to user_preferences")

async def init_db():
    logger.info("🔧 Initializing database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database ready!")
    await fix_missing_columns()

async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    for router in [start_router, profile_router, donate_router, pension_router,
                   useless_router, admin_router, menu_router, budget_router,
                   wallet_router, onboarding_router, gamification_router, webapp_router,
                   dashboard_simple_router]:
        dp.include_router(router)
    logger.info("🚀 Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
