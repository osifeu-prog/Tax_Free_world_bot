from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select

router = Router()

async def set_user_lang(uid: int, lang: str):
    async with async_session() as s:
        stmt = select(User).where(User.telegram_id == uid)
        u = (await s.execute(stmt)).scalar_one_or_none()
        if u: u.language = lang
        else:
            u = User(telegram_id=uid, language=lang)
            s.add(u)
        await s.commit()

@router.message(Command("start"))
async def cmd_start(msg: Message):
    # וודא משתמש קיים
    await set_user_lang(msg.from_user.id, "he")  # ברירת מחדל
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🇮🇱 עברית", callback_data="lang_he"),
        InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en"),
        InlineKeyboardButton(text="🇪🇸 Español", callback_data="lang_es"),
        InlineKeyboardButton(text="🇫🇷 Français", callback_data="lang_fr"),
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton(text="🇸🇦 العربية", callback_data="lang_ar")
    ]])
    await msg.answer(
        "🚀 <b>ברוכים הבאים ל-TON Israel!</b>\n\n"
        "בונים עולם חופשי, חכם ומבוזר.\n\n"
        "📌 <b>התחל עכשיו:</b> /menu  תפריט ראשי\n"
        "📚 <b>אקדמיה:</b> /academy\n"
        "🔗 <b>שתף:</b> /qr\n\n"
        "<i>בחר/י שפה:</i>",
        parse_mode="HTML", reply_markup=kb
    )

@router.callback_query(F.data.startswith("lang_"))
async def lang_callback(c: CallbackQuery):
    lang = c.data.split("_")[1]
    await set_user_lang(c.from_user.id, lang)
    names = {"he":"עברית","en":"English","es":"Español","fr":"Français","ru":"Русский","ar":"العربية"}
    await c.answer(f"✅ השפה נשמרה: {names.get(lang, lang)}", show_alert=True)
    await c.message.edit_reply_markup()
    await c.message.answer("✅ השפה נשמרה בהצלחה!")
