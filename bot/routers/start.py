from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from bot.database.models import User
from bot.services.translation_service import translator
from sqlalchemy import select

router = Router()

@router.message(Command("start"))
async def cmd_start(msg: Message):
    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == msg.from_user.id)
        user = (await session.execute(stmt)).scalar_one_or_none()
        if not user:
            user = User(telegram_id=msg.from_user.id, language="he")
            session.add(user)
            await session.commit()
        lang = user.language or "he"
    
    welcome_text = translator.t(lang, "welcome")
    await msg.answer(welcome_text)
