from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.config import settings

router = Router()

@router.message(Command("export"))
async def cmd_export(msg: Message):
    admin_ids = settings.ADMIN_IDS if hasattr(settings, 'ADMIN_IDS') else []
    if msg.from_user.id not in admin_ids:
        await msg.answer("⛔ גישת אדמין בלבד")
        return
    await msg.answer("📤 ייצוא נתונים - ישלח בקרוב")