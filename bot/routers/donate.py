from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command('donate'))
async def cmd_donate(msg: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💚 50", callback_data="donate_50")],
        [InlineKeyboardButton(text="💚 100", callback_data="donate_100")],
        [InlineKeyboardButton(text="💎 500", callback_data="donate_500")],
        [InlineKeyboardButton(text="💎 TON", callback_data="donate_ton")]
    ])

    await msg.answer(
        "💖 <b>תרומה לפרויקט TON Israel</b>\n\n"
        "הפרויקט חופשי ומתוחזק על ידי קהילה.\n"
        "כל תרומה עוזרת לנו להמשיך לפתח ולשפר.",
        reply_markup=keyboard
    )
