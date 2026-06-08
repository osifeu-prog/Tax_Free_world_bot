from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from bot.database.models import Course, User
from sqlalchemy import select
from bot.services.translation_service import translator

router = Router()

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else "he"

@router.message(Command("academy"))
async def cmd_academy(msg: Message):
    lang = await get_lang(msg.from_user.id)
    async with async_session() as session:
        courses = (await session.execute(select(Course))).scalars().all()
        if not courses:
            await msg.answer(translator.t(lang, "no_courses"))
        else:
            text = translator.t(lang, "academy_title") + "\n\n" + translator.t(lang, "academy_select") + "\n"
            for c in courses:
                text += f"📖 {c.title}\n"
            await msg.answer(text, parse_mode="HTML")
