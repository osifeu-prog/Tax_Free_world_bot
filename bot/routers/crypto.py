from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
from bot.services.translation_service import translator

router = Router()

async def get_lang(uid: int):
    async with async_session() as s:
        stmt = select(User).where(User.telegram_id == uid)
        u = (await s.execute(stmt)).scalar_one_or_none()
        return u.language if u and u.language else "he"

@router.message(Command("crypto"))
async def cmd_crypto(msg: Message):
    lang = await get_lang(msg.from_user.id)
    text = (
        translator.t(lang, "crypto_title") + "\n\n" +
        translator.t(lang, "crypto_body") + "\n\n" +
        translator.t(lang, "crypto_footer")
    )
    await msg.answer(text, parse_mode="HTML")
