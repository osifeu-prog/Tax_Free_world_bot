import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from bot.database.session import engine
from bot.database.models import Base
from bot.routers import start, profile, donate, pension, setwallet, useless, admin, lang
from bot.middlewares.logging_middleware import LoggingMiddleware
from bot.middlewares.useless_middleware import UselessMiddleware

logging.basicConfig(level=logging.INFO)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables initialized")

async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(UselessMiddleware())
    dp.include_routers(
        start.router,
        profile.router,
        donate.router,
        pension.router,
        setwallet.router,
        useless.router,
        admin.router,
        lang.router
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
