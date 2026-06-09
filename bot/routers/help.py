from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
router = Router()
@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer("❔ עזרה - השתמש בפקודות /menu")
