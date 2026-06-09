# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.memory_service import get_user_memory
from bot.keyboards.inline import back_to_main

router = Router()

@router.message(Command("mydata"))
async def cmd_mydata(msg: Message):
    mem = await get_user_memory(msg.from_user.id)
    if not mem:
        await msg.answer("אין עדיין נתונים שמורים. התחל ב-/compare.")
        return
    text = (
        f"📋 <b>הנתונים שלי</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🕹 הפקודה האחרונה: <code>{mem.last_command}</code>\n"
        f"📥 פרמטרים: {mem.last_params}\n"
        f"📤 תוצאה:\n{mem.last_result}\n"
        f"🕒 עדכון אחרון: {mem.updated_at.strftime('%d/%m/%Y %H:%M')}"
    )
    await msg.answer(text, parse_mode="HTML", reply_markup=back_to_main())

