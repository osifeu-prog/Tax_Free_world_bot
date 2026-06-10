import time
from collections import defaultdict
from aiogram import BaseMiddleware
from aiogram.types import Message

class RateLimiter(BaseMiddleware):
    def __init__(self, max_per_second=2):
        self.max_per_second = max_per_second
        self.users = defaultdict(list)
        super().__init__()

    async def __call__(self, handler, event: Message, data):
        uid = event.from_user.id
        now = time.monotonic()
        self.users[uid] = [t for t in self.users[uid] if now - t < 1.0]
        if len(self.users[uid]) >= self.max_per_second:
            await event.answer("⏳ לאט לאט... ממילא אין לאן למהר.")
            return
        self.users[uid].append(now)
        return await handler(event, data)