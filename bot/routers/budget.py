# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.budget import budget_message

router = Router()

@router.message(Command("budget"))
async def cmd_budget(msg: Message):
    parts = msg.text.split()
    if len(parts) < 2:
        await msg.answer("שימוש: /budget <הכנסה חודשית>\nדוגמה: /budget 12000", parse_mode=None)
        return
    try:
        income = float(parts[1])
    except ValueError:
        await msg.answer("הכנסה לא תקינה. דוגמה: /budget 12000", parse_mode=None)
        return
    # budget_message מחזירה טקסט רגיל (ללא HTML)
    await msg.answer(budget_message(income), parse_mode=None)
