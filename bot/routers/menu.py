from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.translation_service import translator
router = Router()

@router.message(Command("menu"))
async def cmd_menu(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 חיסכון & תקציב", callback_data="cmd_budget")],
        [InlineKeyboardButton(text="📊 פנסיה", callback_data="cmd_pension")],
        [InlineKeyboardButton(text="🎓 אקדמיה", callback_data="cmd_academy")],
        [InlineKeyboardButton(text="🏙️ TON City", callback_data="cmd_city")],
        [InlineKeyboardButton(text="🔗 הפניה", callback_data="cmd_ref")],
        [InlineKeyboardButton(text="💖 תרומה", callback_data="cmd_donate")],
        [InlineKeyboardButton(text="❔ עזרה", callback_data="cmd_help")]
    ])
    await msg.answer("📋 <b>תפריט ראשי</b>", parse_mode="HTML", reply_markup=kb)
