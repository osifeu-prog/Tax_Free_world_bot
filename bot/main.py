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

async def ai_handler(message: Message, user_language: str = "he", user_data: dict = None):
    if user_data is None:
        user_data = {}
    response = await llm.get_response(message, user_data)
    await message.reply(response)

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.message.middleware(LanguageMiddleware())
    dp.callback_query.middleware(LanguageMiddleware())

    # AI Handler - רגיש יותר
    dp.message(lambda m: m.text and (
        m.text.startswith(('/ai', 'יוסלס', 'שאל')) or len(m.text.strip()) > 10
    ))(ai_handler)

    logger.info("🚀 @Tax_Free_world_bot עם AI מלא (Gemini)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
