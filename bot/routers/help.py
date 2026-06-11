from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.message(Command("help"))
async def cmd_help(msg: Message):
    help_text = (
        "📋 <b>עזרה  Tax Free World Bot</b>\n\n"
        "<b>פקודות בסיסיות:</b>\n"
        "/start  התחלה / Onboarding\n"
        "/home  מסך הבית\n"
        "/profile  הפרופיל שלי\n"
        "/setwallet  חיבור ארנק TON\n"
        "/language  שינוי שפה\n\n"
        "<b>פיננסים:</b>\n"
        "/adde  הוספת הוצאה\n"
        "/budget  תקציב חודשי\n"
        "/pension  מחשבון פנסיה\n\n"
        "<b>קהילה:</b>\n"
        "/academy  אקדמיה פיננסית\n"
        "/familygroup  קבוצה משפחתית\n"
        "/top  טבלת מובילים\n\n"
        "<b>אחר:</b>\n"
        "/donate  תרומה לפרויקט\n"
        "/useless  AI יוסלס\n"
        "/app  Mini App"
    )
    await msg.answer(help_text, parse_mode="HTML")
