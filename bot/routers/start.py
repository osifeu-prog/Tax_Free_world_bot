from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
from bot.services.translation_service import translator

router = Router()

async def get_lang(user_id: int) -> str:
    async with async_session() as s:
        user = (await s.execute(select(User).where(User.telegram_id == user_id))).scalar_one_or_none()
        return user.language if user and user.language else "he"

@router.message(Command("start"))
async def cmd_start(msg: Message):
    lang = await get_lang(msg.from_user.id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇮🇱 עברית", callback_data="lang_he"),
         InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
         InlineKeyboardButton(text="🇸🇦 العربية", callback_data="lang_ar")],
        [InlineKeyboardButton(text="🇪🇸 Español", callback_data="lang_es"),
         InlineKeyboardButton(text="🇫🇷 Français", callback_data="lang_fr")],
    ])
    await msg.answer(translator.t(lang, "welcome_message"), parse_mode="HTML", reply_markup=kb)

@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    uid = callback.from_user.id
    async with async_session() as session:
        user = (await session.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        if user:
            user.language = lang
        else:
            session.add(User(telegram_id=uid, language=lang))
        await session.commit()
    await callback.message.edit_text(translator.t(lang, "welcome_message"), parse_mode="HTML")
    from bot.routers.menu import get_menu_text, get_main_keyboard
    menu_text = await get_menu_text(lang)
    kb = get_main_keyboard(lang)
    await callback.message.answer(menu_text, parse_mode="HTML", reply_markup=kb)
    await callback.answer()
