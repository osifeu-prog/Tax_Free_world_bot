from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
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
    return translator.t(lang, "menu_title") + "\n\n" + \
           translator.t(lang, "pension_promo") + "\n" + \
           translator.t(lang, "academy_promo") + "\n" + \
           translator.t(lang, "share_qr") + "\n" + \
           translator.t(lang, "household_promo") + "\n" + \
           translator.t(lang, "donate_promo")

@router.message(Command("menu"))
async def cmd_menu(msg: Message):
    lang = await get_lang(msg.from_user.id)
    await msg.answer(await get_menu_text(lang), parse_mode="HTML")
