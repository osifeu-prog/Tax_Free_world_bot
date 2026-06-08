from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from bot.database.models import UserProgress, User
from sqlalchemy import select
from bot.services.translation_service import translator

router = Router()

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else "he"

@router.message(Command("myprogress"))
async def cmd_myprogress(msg: Message):
    lang = await get_lang(msg.from_user.id)
    async with async_session() as session:
        rows = (await session.execute(select(UserProgress).where(UserProgress.telegram_id == msg.from_user.id))).scalars().all()
        if not rows:
            await msg.answer(translator.t(lang, "no_courses"))
            return
        text = f"<b>{translator.t(lang, 'progress_title')}</b>\n"
        for r in rows:
            text += f"📖 קורס {r.course_id}: {r.score} נקודות\n"
        await msg.answer(text, parse_mode="HTML")
