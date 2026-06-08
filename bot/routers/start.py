from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
from bot.services.translation_service import translator

router = Router()

async def set_user_lang(uid: int, lang: str):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        if u:
            u.language = lang
        else:
            u = User(telegram_id=uid, language=lang)
            s.add(u)
        await s.commit()

@router.message(Command("start"))
async def cmd_start(msg: Message):
    lang = msg.from_user.language_code or "he"
    await set_user_lang(msg.from_user.id, lang)
    welcome = translator.t(lang, "welcome")
    await msg.answer(welcome, parse_mode="HTML")
    await msg.answer(f"{translator.t(lang, 'menu_prompt')} /menu", parse_mode="HTML")
