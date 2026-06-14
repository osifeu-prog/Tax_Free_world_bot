import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.middlewares.language_middleware import LanguageMiddleware

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Language Middleware
    dp.message.middleware(LanguageMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())

    # Routers בסיסיים
    try:
        from bot.routers.start import router as router_start
        dp.include_router(router_start)
    except:
        pass

    try:
        from bot.routers.help import router as router_help
        dp.include_router(router_help)
    except:
        pass

    try:
        from bot.routers.profile import router as router_profile
        dp.include_router(router_profile)
    except:
        pass

    logger.info(f"🚀 @Tax_Free_world_bot started successfully with AI + I18N support")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
