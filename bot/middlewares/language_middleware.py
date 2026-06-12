from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from bot.language_detector import get_user_language

class LanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        text = ""
        if isinstance(event, Message):
            text = event.text or event.caption or ""
        elif isinstance(event, CallbackQuery):
            text = event.data or ""

        if not text:
            return await handler(event, data)

        user_data = data.get("user_data") or {}
        preferred_lang = user_data.get("language")

        detected_lang = get_user_language(text, preferred_lang)
        data["user_language"] = detected_lang

        return await handler(event, data)
