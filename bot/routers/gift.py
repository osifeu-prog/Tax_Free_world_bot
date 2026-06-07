from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.messages.he import MESSAGES
import random

router = Router()

@router.message(Command("gift"))
async def cmd_gift(msg: Message):
    tip = random.choice(MESSAGES["tips"])
    await msg.answer(MESSAGES["gift"].format(random_tip=tip), parse_mode="HTML")
