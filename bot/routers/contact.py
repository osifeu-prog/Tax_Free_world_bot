# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("contact"))
async def cmd_contact(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 שלח הודעה לאוסיף", url="https://t.me/+1ANn25HeVBoxNmRk")],
    ])
    await msg.answer(
        "📬 <b>צור קשר</b>\n\nאפשר לפנות אליי ישירות:",
        parse_mode="HTML",
        reply_markup=kb
    )

