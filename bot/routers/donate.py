from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy import text as sa_text
from bot.database.session import engine

router = Router()

@router.message(Command('donate'))
async def cmd_donate(msg: Message):
    await msg.answer("💖 תרומה לבוט\n\nשלח סכום או לחץ על כפתור:", 
                     reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                         [InlineKeyboardButton(text="50 ", callback_data="donate_50")],
                         [InlineKeyboardButton(text="100 ", callback_data="donate_100")],
                         [InlineKeyboardButton(text="500 ", callback_data="donate_500")]
                     ]))

@router.callback_query(lambda c: c.data.startswith("donate_"))
async def process_donate(callback: CallbackQuery):
    amount = int(callback.data.split("_")[1])
    await callback.message.edit_text(f"✅ תודה על תרומה של {amount} !")
    # TODO: כאן תוסיף לוגיקה של הוספת תרומה
