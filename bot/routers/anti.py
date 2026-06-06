from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("anti"))
async def cmd_anti(msg: Message):
    await msg.answer(MESSAGES["anti"], parse_mode="HTML")
