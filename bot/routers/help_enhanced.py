# שיפור /help  מציג פקודות לפי קטגוריות
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

COMMAND_CATEGORIES = {
    "💰 Wealth": ["/budget", "/pension", "/report_pension", "/setincome", "/compare", "/wallet", "/mysavings"],
    "🎓 Learn": ["/academy", "/crypto", "/cbdc", "/decentral", "/socio", "/anti", "/edu", "/academy_extended", "/academy_nft", "/academy_dao", "/vision", "/spark", "/course_progress", "/seed_courses"],
    "🤖 AI": ["/useless", "/ask", "/ai"],
    "🌍 Community": ["/ref", "/qr", "/stats", "/top", "/tip", "/contact", "/faq", "/daily", "/mydata", "/gift", "/familygroup", "/household", "/shopping", "/chore"],
    "🎁 Rewards": ["/daily", "/ref", "/top", "/gift"],
    "👤 Profile": ["/profile", "/setwallet", "/language"],
    "🛠️ Utilities": ["/help", "/menu", "/keyboard", "/hide", "/feedback", "/quiz", "/architecture", "/whyus", "/familyguide"],
    "💖 Donate": ["/donate"]
}

@router.message(Command("help"))
async def enhanced_help(msg: Message):
    text = "📖 <b>Tax Free World  כל הפקודות לפי נושא</b>\n\n"
    for category, commands in COMMAND_CATEGORIES.items():
        text += f"<b>{category}</b>\n"
        text += " ".join(commands) + "\n\n"
    text += "➡️ /guide  מדריך מהיר\n➡️ /start  התחל מחדש"
    await msg.answer(text, parse_mode="HTML")
