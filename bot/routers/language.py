from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select

router = Router()

@router.message(Command("language"))
async def cmd_language(msg: Message):
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
    await msg.answer("🌐 בחר/י שפה:", reply_markup=kb)

@router.callback_query(F.data.startswith("lang_"))
async def lang_callback(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == callback.from_user.id))).scalar_one_or_none()
        if u:
            u.language = lang
        else:
            u = User(telegram_id=callback.from_user.id, language=lang)
            s.add(u)
        await s.commit()
    names = {"he":"עברית","en":"English","es":"Español","fr":"Français","ru":"Русский","ar":"العربية"}
    await callback.answer(f"✅ {names.get(lang, lang)}", show_alert=True)
    await callback.message.edit_reply_markup()

