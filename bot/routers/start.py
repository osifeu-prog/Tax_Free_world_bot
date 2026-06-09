from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
from bot.services.translation_service import translator
router = Router()

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u else "he"

@router.message(Command("start"))
async def cmd_start(msg: Message):
    lang = await get_lang(msg.from_user.id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 מחשבון", callback_data="open_miniapp")],
        [InlineKeyboardButton(text="💰 חיסכון", callback_data="go_budget"),
         InlineKeyboardButton(text="📊 פנסיה", callback_data="go_pension")],
        [InlineKeyboardButton(text="🎓 אקדמיה", callback_data="go_academy")]
    ])
    await msg.answer(translator.t(lang, "welcome_message", name=msg.from_user.first_name or "חבר"), parse_mode="HTML", reply_markup=kb)
