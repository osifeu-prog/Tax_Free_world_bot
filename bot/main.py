import asyncio
from aiogram import Bot, Dispatcher
from bot.config import settings
from bot.utils.logger import logger
from bot.database.models import Base
from bot.database.session import engine
from bot.routers import routers

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized.")

async def main():
    await init_db()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    for router in routers:
        dp.include_router(router)
    logger.info("Bot started. Polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
