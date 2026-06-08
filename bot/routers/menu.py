from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from bot.database.models import User
from bot.services.translation_service import translator
from sqlalchemy import select

router = Router()

@router.message(Command("menu"))
async def cmd_menu(msg: Message):
    async with async_session() as session:
        stmt = select(User.language).where(User.telegram_id == msg.from_user.id)
        lang = (await session.execute(stmt)).scalar_one_or_none()
        lang = lang or "he"
    
    menu_text = translator.t(lang, "menu_text")
    await msg.answer(menu_text, parse_mode="HTML")
