import random
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

QUIZ = [
    ("מהי העמלה הממוצעת של ביט?", "1.5%"),
    ("מהי העמלה של TON?", "0.1%"),
    ("האם TON חוקי בישראל?", "כן"),
    ("איפה פותחים ארנק TON?", "ב-@wallet"),
]

@router.message(Command("quiz"))
async def cmd_quiz(msg: Message):
    q, a = random.choice(QUIZ)
    await msg.answer(f"❓ <b>חידון:</b>\n{q}\n\nהקלד את התשובה!")
    # שמירת התשובה הנכונה ב-state
    # (בגרסה פשוטה, נשתמש במעקב הודעה)
    # למימוש מלא יש צורך ב-FSM  נשאיר לגרסה הבאה
