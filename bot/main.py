import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.database.session import engine
from bot.database.models import Base

# ייבוא הראוטרים שלך
from bot.routers.start import router as start_router
from bot.routers.profile import router as profile_router
from bot.routers.donate import router as donate_router
from bot.routers.pension import router as pension_router
from bot.routers.useless import router as useless_router
from bot.routers.admin import router as admin_router
# הוסף כאן ראוטרים נוספים אם יש

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db():
    logger.info("🔧 Initializing database tables...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ All database tables initialized successfully!")
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
