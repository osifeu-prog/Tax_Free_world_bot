from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
router = Router()
@router.message(Command("academy"))
async def cmd_academy(msg: Message):
    await msg.answer("🎓 אקדמיה - תוכן מלא בקרוב")
