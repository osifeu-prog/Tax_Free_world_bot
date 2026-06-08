from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
from bot.services.translation_service import translator

router = Router()

async def set_user_lang(telegram_id: int, lang: str):
    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        user = (await session.execute(stmt)).scalar_one_or_none()
        if user:
            user.language = lang
        else:
            user = User(telegram_id=telegram_id, language=lang)
            session.add(user)
        await session.commit()

async def get_user_lang(telegram_id: int) -> str:
    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        user = (await session.execute(stmt)).scalar_one_or_none()
        return user.language if user and user.language else "he"

@router.message(Command("start"))
async def cmd_start(msg: Message):
    lang = await get_user_lang(msg.from_user.id)
    # כפתורי בחירת שפה
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇮🇱 עברית", callback_data="lang_he"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
            InlineKeyboardButton(text="🇪🇸 Español", callback_data="lang_es"),
            InlineKeyboardButton(text="🇫🇷 Français", callback_data="lang_fr"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇸🇦 العربية", callback_data="lang_ar")
        ]
    ])
    welcome = translator.t(lang, "welcome")
    choose = translator.t(lang, "choose_language")
    await msg.answer(f"{welcome}\n\n{choose}", reply_markup=kb)

@router.callback_query(lambda c: c.data and c.data.startswith("lang_"))
async def lang_callback(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    await set_user_lang(callback.from_user.id, lang)
    saved = translator.t(lang, "language_saved")
    await callback.answer(saved, show_alert=True)
    # כעת שלח הודעת התחלה בשפה החדשה
    welcome = translator.t(lang, "welcome")
    await callback.message.answer(welcome)
