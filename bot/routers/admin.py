from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import settings

router = Router()

@router.message(Command("admin"))
async def cmd_admin(msg: Message):
    if msg.from_user.id not in settings.admin_ids:
        await msg.answer("⛔ אין לך הרשאות גישה לאזור זה.")
        return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 ייצוא לוגים", callback_data="export_csv")],
        [InlineKeyboardButton(text="📈 סטטיסטיקות", callback_data="stats")],
        [InlineKeyboardButton(text="🔄 רענון", callback_data="start")],
    ])
    await msg.answer("🔐 <b>אזור אדמין</b>", parse_mode="HTML", reply_markup=kb)
