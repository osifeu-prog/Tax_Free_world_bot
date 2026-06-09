from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.translation_service import translator
router = Router()
@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer("📖 עזרה  בקרוב")
