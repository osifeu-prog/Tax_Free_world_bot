# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.ai_service import ask_ai
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("ai"))
async def cmd_ai(msg: Message):
    question = msg.text.split(maxsplit=1)
    if len(question) == 1:
        await msg.answer("🤖 <b>שימוש:</b> <code>/ai איך לחסוך בעמלות?</code>", parse_mode="HTML")
        return
    await msg.answer("🤖 <i>חושב...</i>", parse_mode="HTML")
    answer = await ask_ai(question[1])
    await msg.answer(answer)

@router.message(Command("menu"))
async def cmd_menu(msg: Message):
    menu_text = '''
🗺️ <b>מפת האתר  TON Israel</b>

💰 <b>חיסכון:</b>
/start, /compare, /wallet, /why, /business

🏠 <b>ניהול כלכלת הבית:</b>
/budget, /profile, /addexpense, /expenses, /setincome, /delexpense, /household

📚 <b>אקדמיה:</b>
/crypto, /cbdc, /decentral, /socio, /anti, /edu, /academy_extended, /academy_nft, /academy_dao

👥 <b>קהילה:</b>
/ref, /stats, /top, /tip, /contact, /id, /daily, /mydata, /gift

🛠️ <b>כלים:</b>
/miniapp, /keyboard, /hide, /ask, /feedback, /help, /quiz, /ai, /architecture

⭐ <b>אודות:</b>
/whyus, /familyguide

🔐 <b>הרשאות:</b>
/requestadmin, /addadmin, /login, /setpassword, /removeadmin

🔒 <b>אדמין:</b>
/admin, /export, /debug
'''
    await msg.answer(menu_text, parse_mode="HTML")

@router.message(Command("whyus"))
async def cmd_whyus(msg: Message):
    await msg.answer(MESSAGES["whyus"], parse_mode="HTML")

@router.message(Command("familyguide"))
async def cmd_familyguide(msg: Message):
    await msg.answer(MESSAGES["familyguide"], parse_mode="HTML")

