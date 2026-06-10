from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from bot.database.session import async_session
from sqlalchemy import text

router = Router()

def get_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ הוצאה"), KeyboardButton(text="💰 הכנסה")],
            [KeyboardButton(text="📊 פנסיה"), KeyboardButton(text="💖 תרומה")],
            [KeyboardButton(text="🎓 אקדמיה"), KeyboardButton(text="🤖 AI")],
            [KeyboardButton(text="📋 עזרה")]
        ],
        resize_keyboard=True
    )

@router.message(Command('start'))
async def cmd_start(msg: Message):
    uid = msg.from_user.id
    async with async_session() as s:
        prefs = await s.execute(text("SELECT onboarding_completed FROM user_preferences WHERE user_id = :uid"), {"uid": uid})
        row = prefs.fetchone()
        if row and row[0]:
            await msg.answer("🏠 ברוך הבא! השתמש ב-/menu לתפריט ראשי.", reply_markup=get_reply_keyboard())
            return
    await msg.answer("🌍 ברוכים הבאים ל-Tax Free World!\n\nאנו נשמח לעזור לך לנהל כספים, לחסוך ולהשקיע.\nשלח /menu להתחלה!", reply_markup=get_reply_keyboard())
    # שמירה מהירה שהמשתמש ראה את ההודעה (ללא onboarding מורכב)
    await s.execute(text("INSERT OR IGNORE INTO user_preferences (user_id, onboarding_completed) VALUES (:uid, 1)"), {"uid": uid})
    await s.commit()
