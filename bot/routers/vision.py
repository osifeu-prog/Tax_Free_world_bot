from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
router = Router()
@router.message(Command("vision"))
async def cmd_vision(msg: Message):
    await msg.answer("🔭 חזון")
