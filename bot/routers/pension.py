from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
router = Router()
@router.message(Command("pension"))
async def cmd_pension(msg: Message):
    await msg.answer("📊 מחשבון פנסיה - התחל /pension")
