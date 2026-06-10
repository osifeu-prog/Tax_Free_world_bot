from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

class AdminOnlyMiddleware(BaseMiddleware):
    ADMIN_IDS = [224223270, 8789977826]  # עדכן לפי הצורך
    HIDDEN_COMMANDS = ["/dbstats", "/debug", "/fix_users", "/health", "/export", "/addgroup", "/groups", "/setrole", "/report", "/admin"]

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.text and event.text.startswith("/"):
            cmd = event.text.split()[0]
            if cmd in self.HIDDEN_COMMANDS and event.from_user.id not in self.ADMIN_IDS:
                return  # פקודה חסומה, לא עושים כלום
        return await handler(event, data)
