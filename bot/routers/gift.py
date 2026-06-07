import asyncio
import random
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.points_service import add_points

router = Router()

PRIZES = [
    (0, "כלום... נסה שוב!"),
    (10, "10 נקודות!"),
    (20, "20 נקודות!"),
    (50, "50 נקודות!"),
    (100, "100 נקודות! 🎉"),
    (200, "200 נקודות! 🌟"),
]

@router.message(Command("gift"))
async def cmd_gift(msg: Message):
    dice = await msg.answer_dice(emoji="🎰")
    prize = random.choices(PRIZES, weights=[30,25,20,15,7,3], k=1)[0]
    points, text = prize
    if points > 0:
        total = await add_points(msg.from_user.id, points)
        result = f"🎁 {text}\nיש לך עכשיו {total} נקודות!"
    else:
        result = f"😕 {text}"
    await asyncio.sleep(3)
    await dice.edit_text(result)
