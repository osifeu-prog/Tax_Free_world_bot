from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("edu"))
async def cmd_edu(msg: Message):
    await msg.answer(MESSAGES["edu"], parse_mode="HTML")
