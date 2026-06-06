from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("decentral"))
async def cmd_decentral(msg: Message):
    await msg.answer(MESSAGES["decentral"], parse_mode="HTML")
