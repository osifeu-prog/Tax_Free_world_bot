# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.messages.he import MESSAGES

router = Router()

FAQ_ANSWERS = {
    "איך פותחים ארנק": "/wallet",
    "כמה עולה העברה": "/compare 500 10",
    "מה זה ton": "/why",
    "איך לחסוך": "/compare",
    "קריפטו": "/crypto",
    "cbdc": "/cbdc",
    "ביזור": "/decentral",
    "סוציוקרטיה": "/socio",
    "nft": "/academy_nft",
    "dao": "/academy_dao",
    "תרומה": "/donate",
    "סטטיסטיקות": "/stats",
    "לוח מובילים": "/top",
    "תקציב": "/budget 12000",
    "צור קשר": "/contact",
    "עזרה": "/help",
}

@router.message(Command("ask"))
async def cmd_ask(msg: Message):
    question = msg.text.split(maxsplit=1)
    if len(question) == 1:
        await msg.answer("🤖 <b>שאל כל שאלה!</b>\nנסה: <code>/ask איך לחסוך בעמלות?</code>")
        return
    q = question[1].lower()
    for key, response in FAQ_ANSWERS.items():
        if key in q:
            await msg.answer(f"🔍 מצאתי תשובה:\nהשתמש בפקודה {response}")
            return
    await msg.answer("לא מצאתי תשובה מדויקת.\nשלח /feedback ונשמח לעזור!")

