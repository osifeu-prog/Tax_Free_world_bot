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
from bot.routers.menu import router as menu_router
from bot.routers.dashboard_simple import router as dashboard_router
from bot.routers.profile import router as profile_router
from bot.routers.wallet import router as wallet_router
from bot.routers.budget import router as budget_router
from bot.routers.donate import router as donate_router
from bot.routers.pension import router as pension_router
from bot.routers.gamification import router as gamification_router
from bot.routers.webapp import router as webapp_router
from bot.routers.import_users import router as import_router
from bot.routers.help import router as help_router

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    for router in [start_router, menu_router, dashboard_router, profile_router, 
                   wallet_router, budget_router, donate_router, pension_router,
                   gamification_router, webapp_router]:
        dp.include_router(router)
    
    logger.info("🚀 Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

