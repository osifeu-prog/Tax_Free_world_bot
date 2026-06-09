from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.translation_service import translator
router = Router()
@router.message(Command("academy"))
async def cmd_academy(msg: Message):
    await msg.answer("🎓 אקדמיה  בקרוב")
