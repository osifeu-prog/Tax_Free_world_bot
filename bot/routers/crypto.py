from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.translation_service import translator
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select

router = Router()

async def get_user_lang(telegram_id: int) -> str:
    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        user = (await session.execute(stmt)).scalar_one_or_none()
        return user.language if user and user.language else "he"

@router.message(Command("crypto"))
async def cmd_crypto(msg: Message):
    lang = await get_user_lang(msg.from_user.id)
    text = (
        translator.t(lang, "crypto_title") + "\n\n" +
        translator.t(lang, "crypto_body") + "\n\n" +
        translator.t(lang, "crypto_footer")
    )
    await msg.answer(text, parse_mode="HTML")
