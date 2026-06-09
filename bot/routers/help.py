from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.command_registry import get_commands_by_category
from bot.services.translation_service import translator
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select

router = Router()

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else "he"

@router.message(Command("help"))
async def cmd_help(msg: Message):
    lang = await get_lang(msg.from_user.id)
    cats = get_commands_by_category()
    text = f"📖 <b>{translator.t(lang, 'help_title')}</b>\n\n"
    for cat, cmds in cats.items():
        text += f"<b>{cat}</b>\n"
        for c in cmds:
            text += f"/{c} - {translator.t(lang, f'cmd_{c}')}\n"
        text += "\n"
    await msg.answer(text, parse_mode="HTML")
