from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
from bot.services.translation_service import translator

router = Router()

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else "he"

@router.message(Command("start"))
async def cmd_start(msg: Message):
    lang = await get_lang(msg.from_user.id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇮🇱 עברית", callback_data="lang_he"),
         InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
    ])
    await msg.answer(translator.t(lang, "welcome_message"), parse_mode="HTML", reply_markup=kb)

# ... (המשך כמו קודם)
