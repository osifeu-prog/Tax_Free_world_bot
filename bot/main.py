import asyncio
import logging
import os
from sqlalchemy import text

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.database.session import engine
from bot.database.models import Base

# ====================== ALL ROUTERS ======================



from bot.routers.start import router as start_router
from bot.routers.profile import router as profile_router
from bot.routers.donate import router as donate_router
from bot.routers.pension import router as pension_router
from bot.routers.useless import router as useless_router
from bot.routers.admin import router as admin_router
from bot.routers.menu import router as menu_router

# ניסיון לייבא routers נוספים (אם קיימים)
try:
    from bot.routers.budget import router as budget_router
    BUDGET_EXISTS = True
except ImportError:
    BUDGET_EXISTS = False

try:
    from bot.routers.expense import router as expense_router
    EXPENSE_EXISTS = True
except ImportError:
    EXPENSE_EXISTS = False

try:
    from bot.routers.academy import router as academy_router
    ACADEMY_EXISTS = True
except ImportError:
    ACADEMY_EXISTS = False

try:
    from bot.routers.household import router as household_router
    HOUSEHOLD_EXISTS = True
except ImportError:
    HOUSEHOLD_EXISTS = False
# ========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not set")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def fix_missing_columns():
    async with engine.begin() as conn:
        pragma = await conn.execute(text("PRAGMA table_info(users)"))
        columns = [row[1] for row in pragma.fetchall()]
        logger.info(f"Existing columns in users: {columns}")

        needed = {
            "role": "VARCHAR(20) DEFAULT 'user'",
            "wallet_address": "VARCHAR(255)",
            "points": "FLOAT DEFAULT 0",
            "last_gift_date": "VARCHAR(50)",
            "gift_shares_today": "INTEGER DEFAULT 0"
        }

        for col, definition in needed.items():
            if col not in columns:
                await conn.execute(text(f"ALTER TABLE users ADD COLUMN {col} {definition}"))
                logger.info(f"✅ Column '{col}' added")


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

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(donate_router)
    dp.include_router(pension_router)
    dp.include_router(useless_router)
    dp.include_router(admin_router)
    dp.include_router(menu_router)
    dp.include_router(expenses_router)
    dp.include_router(incomes_router)
    dp.include_router(categories_router)

    if BUDGET_EXISTS: dp.include_router(budget_router)
    if EXPENSE_EXISTS: dp.include_router(expense_router)
    if ACADEMY_EXISTS: dp.include_router(academy_router)
    if HOUSEHOLD_EXISTS: dp.include_router(household_router)

    logger.info("🚀 Bot starting polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())






