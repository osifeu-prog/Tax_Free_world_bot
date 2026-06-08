from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("donate"))
async def cmd_donate(msg: Message):
    text = """
💖 <b>תמכו בנו!</b>

TON Israel היא קהילה חופשית  ללא מימון ממשלתי.
אם הבוט עוזר לך, תוכל לתרום:

👛 <b>ארנק TON:</b>
<code>EQD... (הכנס כתובת ארנק משלך)</code>

🔗 או שתף את הקישור שלך: /qr

🙏 תודה על התמיכה!
"""
    await msg.answer(text, parse_mode="HTML")
