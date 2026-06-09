from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
router = Router()

@router.message(Command("admin"))
async def cmd_admin(msg: Message):
    await msg.answer("🔒 <b>ניהול מערכת TON Israel</b>\n\n/admin  פאנל אדמין\n/export  ייצוא נתונים\n/debug  מצב דיבאג", parse_mode="HTML")