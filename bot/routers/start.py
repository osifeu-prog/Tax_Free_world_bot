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
    # שלח תפריט
    from bot.routers.menu import get_menu_text
    menu_text = await get_menu_text(lang)
    await callback.message.answer(menu_text, parse_mode="HTML")
    # כפתור סיור
    tour_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translator.t(lang, "tour_title"), callback_data="start_tour")]
    ])
    await callback.message.answer("✅ " + translator.t(lang, "choose_language"), reply_markup=tour_kb)
    await callback.answer()

@router.callback_query(F.data == "start_tour")
async def start_tour(callback: CallbackQuery):
    lang = await get_lang(callback.from_user.id)
    steps = [
        translator.t(lang, "tour_step1"),
        "2️⃣ " + translator.t(lang, "academy_promo"),
        "3️⃣ " + translator.t(lang, "share_qr"),
        "4️⃣ " + translator.t(lang, "household_promo"),
        "5️⃣ " + translator.t(lang, "donate_promo"),
    ]
    for step in steps:
        await callback.message.answer(step)
    await callback.answer()
