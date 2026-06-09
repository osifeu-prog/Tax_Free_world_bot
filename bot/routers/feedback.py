# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.config import settings

router = Router()

ADMIN_CHAT_ID = settings.admin_ids[0] if settings.admin_ids else 224223270

@router.message(Command("feedback"))
async def cmd_feedback(msg: Message):
    text = msg.text.split(maxsplit=1)
    if len(text) == 1:
        await msg.answer("📝 <b>שלח דיווח:</b>\nהשתמש בתבנית: <code>/feedback הטקסט שלך</code>")
        return
    report = text[1]
    await msg.bot.send_message(
        ADMIN_CHAT_ID,
        f"📥 <b>דיווח חדש:</b>\nמאת: {msg.from_user.first_name} (ID: {msg.from_user.id})\n\n{report}",
        parse_mode="HTML"
    )
    await msg.answer("✅ <b>הדיווח נשלח!</b> תודה על תרומתך.")

