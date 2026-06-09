from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.translation_service import translator
router = Router()
@router.message(Command("menu"))
async def cmd_menu(msg: Message):
    await msg.answer("📋 תפריט ראשי - השתמש ב/start")
