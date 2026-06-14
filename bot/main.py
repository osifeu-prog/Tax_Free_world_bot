import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

from bot.middlewares.language_middleware import LanguageMiddleware
from bot.llm_router import LLMRouter

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = LLMRouter()

async def ai_handler(message: Message, user_language: str, user_data: dict):
    response = await llm.get_response(message, user_data)
    await message.reply(response)

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Middleware
    dp.message.middleware(LanguageMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())

    # AI Handler
    dp.message(lambda m: m.text and (m.text.startswith(('/ai', 'יוסלס', 'שאל')) or len(m.text) > 15))(ai_handler)

    # ניסיון לטעון routers נוספים (בלי לקרוס)
    routers = ['start', 'help', 'profile', 'menu', 'language', 'top', 'whyus']
    for r in routers:
        try:
            module = __import__(f"bot.routers.{r}", fromlist=["router"])
            dp.include_router(module.router)
            logger.info(f"✅ Loaded router: {r}")
        except Exception as e:
            logger.warning(f"⚠️ Could not load router {r}: {e}")

    logger.info("🚀 @Tax_Free_world_bot started with AI + I18N")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
