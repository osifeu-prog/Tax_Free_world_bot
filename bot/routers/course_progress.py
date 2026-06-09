from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
router = Router()
@router.message(Command("course_progress"))
async def cmd_course_progress(msg: Message):
    await msg.answer("📈 התקדמות בקורסים")
