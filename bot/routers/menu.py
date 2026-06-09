from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.translation_service import translator
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select

router = Router()

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else "he"

async def get_menu_text(lang: str) -> str:
    return (
        f"🗺️ <b>{translator.t(lang, 'menu_title')}</b>\n\n"
        f"💼 {translator.t(lang, 'pension_promo')}\n"
        f"📚 {translator.t(lang, 'academy_promo')}\n"
        f"🔗 {translator.t(lang, 'share_qr')}\n"
        f"🏠 {translator.t(lang, 'household_promo')}\n"
        f"💖 {translator.t(lang, 'donate_promo')}\n"
    )

def get_main_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translator.t(lang, "cmd_pension"), callback_data="cmd_pension"),
         InlineKeyboardButton(text=translator.t(lang, "cmd_academy"), callback_data="cmd_academy")],
        [InlineKeyboardButton(text=translator.t(lang, "cmd_city"), callback_data="cmd_city"),
         InlineKeyboardButton(text=translator.t(lang, "cmd_market"), callback_data="cmd_market")],
        [InlineKeyboardButton(text=translator.t(lang, "cmd_donate"), callback_data="cmd_donate"),
         InlineKeyboardButton(text=translator.t(lang, "cmd_report"), callback_data="cmd_report")],
        [InlineKeyboardButton(text=translator.t(lang, "cmd_help"), callback_data="cmd_help")],
    ])

@router.message(Command("menu"))
async def cmd_menu(msg: Message):
    lang = await get_lang(msg.from_user.id)
    text = await get_menu_text(lang)
    kb = get_main_keyboard(lang)
    await msg.answer(text, parse_mode="HTML", reply_markup=kb)

@router.callback_query(F.data.startswith("cmd_"))
async def handle_menu_click(callback: CallbackQuery):
    command = callback.data[4:]
    await callback.message.answer(f"/{command}")
    await callback.answer()
