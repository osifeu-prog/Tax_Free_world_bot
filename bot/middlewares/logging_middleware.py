import time, logging
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

logger = logging.getLogger("bot")

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        start = time.monotonic()
        uid = event.from_user.id if event.from_user else "unknown"
        if isinstance(event, Message):
            logger.info(f"📩 {uid}: {event.text[:50] if event.text else '<no text>'}")
        elif isinstance(event, CallbackQuery):
            logger.info(f"🔘 {uid}: {event.data}")
        result = await handler(event, data)
        elapsed = (time.monotonic() - start) * 1000
        logger.info(f"✅ handled in {elapsed:.0f}ms")
        return result
