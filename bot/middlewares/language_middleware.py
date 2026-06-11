from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from bot.services.language_detector import get_user_language

class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, (Message, CallbackQuery)):
            text = event.text or event.data or ""
            user = event.from_user
            if user and text:
                preferred = data.get("user_data", {}).get("language")
                detected = get_user_language(text, preferred)
                data["user_language"] = detected
        return await handler(event, data)
