from aiogram import BaseMiddleware
from aiogram.types import Message
import random

SHARE_PROMPTS = [
    "תשלח אותי למישהו שגם הוא צריך תזכורת שאין משמעות.",
    "שיתוף זה אשליה של תנועה. אבל אם כבר, אז הנה לינק.",
    "תפיץ את הריקנות. לפחות היא עקבית.",
]

class UselessShareMiddleware(BaseMiddleware):
    def __init__(self):
        self.counter = 0
        self.next_trigger = random.randint(3, 19)
        super().__init__()

    async def __call__(self, handler, event: Message, data):
        result = await handler(event, data)
        if hasattr(event, 'text') and event.text and not event.text.startswith('/'):
            self.counter += 1
            if self.counter >= self.next_trigger:
                self.counter = 0
                self.next_trigger = random.randint(3, 19)
                prompt = random.choice(SHARE_PROMPTS)
                ref_link = f"https://t.me/Tax_Free_world_bot?start=ref{event.from_user.id}"
                await event.answer(f"{prompt}\n\n{ref_link}")
        return result