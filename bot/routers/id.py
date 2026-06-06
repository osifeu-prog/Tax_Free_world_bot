from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("id"))
async def cmd_id(msg: Message):
    chat = msg.chat
    user = msg.from_user
    lines = [f"👤 <b>המשתמש</b>: <code>{user.id}</code>"]
    if chat.id != user.id:
        lines.append(f"💬 <b>הקבוצה/ערוץ</b>: <code>{chat.id}</code>")
    await msg.answer("\n".join(lines), parse_mode="HTML")
