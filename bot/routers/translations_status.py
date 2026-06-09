from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
router = Router()
@router.message(Command("translations_status"))
async def cmd_translations_status(msg: Message):
    await msg.answer("🌐 סטטוס תרגומים")
