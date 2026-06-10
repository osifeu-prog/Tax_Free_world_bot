from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import time
from bot.utils.logger_utils import log_command

class DetailedLoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        start = time.perf_counter()
        user_id = event.from_user.id
        text = event.text or "[non-text]"
        try:
            result = await handler(event, data)
            duration = (time.perf_counter() - start) * 1000
            await log_command(user_id, text, "handled", duration)
            return result
        except Exception as e:
            duration = (time.perf_counter() - start) * 1000
            await log_command(user_id, text, "error", duration, str(e))
            raise
