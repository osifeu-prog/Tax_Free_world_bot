from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
from bot.services.translation_service import translator

router = Router()

async def get_user_lang(uid: int) -> str:
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else "he"

@router.message(Command("vision"))
async def cmd_vision(msg: Message):
    lang = await get_user_lang(msg.from_user.id)
    text = (
        translator.t(lang, "vision_title") + "\n\n" +
        translator.t(lang, "vision_body") + "\n\n" +
        translator.t(lang, "vision_footer")
    )
    await msg.answer(text, parse_mode="HTML")
