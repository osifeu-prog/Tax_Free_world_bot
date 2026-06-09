from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
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
    name = msg.from_user.first_name or "חבר"
    welcome = translator.t(lang, "welcome_message", name=name)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇮🇱 עברית", callback_data="lang_he"), InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"), InlineKeyboardButton(text="🇸🇦 العربية", callback_data="lang_ar")],
        [InlineKeyboardButton(text="🇪🇸 Español", callback_data="lang_es"), InlineKeyboardButton(text="🇫🇷 Français", callback_data="lang_fr")],
        [InlineKeyboardButton(text="🇾🇮 יידיש", callback_data="lang_yi")],
        [InlineKeyboardButton(text="📱 מחשבון ויזואלי", callback_data="open_miniapp")],
        [InlineKeyboardButton(text="📋 תפריט מלא", callback_data="show_menu")]
    ])
    await msg.answer(welcome, parse_mode="HTML", reply_markup=kb)

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
    await callback.answer(f"✅ שפה שונתה ל-{lang}")

@router.callback_query(F.data == "show_menu")
async def show_full_menu(callback: CallbackQuery):
    from bot.routers.menu import cmd_menu
    await cmd_menu(callback.message)
    await callback.answer()