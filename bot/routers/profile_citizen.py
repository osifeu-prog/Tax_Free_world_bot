from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.citizen_engine import citizen

router = Router()

@router.message(Command("profile"))
async def cmd_profile(msg: Message):
    profile = await citizen.get_profile(msg.from_user.id)
    text = (
        f"👤 <b>הפרופיל האזרחי שלי</b>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"⭐ רמה: {profile['level']}\n"
        f"✨ XP: {profile['xp']}\n"
        f"📚 מוניטין ידע: {profile['reputation_knowledge']}\n"
        f"🤝 מוניטין קהילתי: {profile['reputation_community']}\n"
        f"🚀 מוניטין מנהיגות: {profile['reputation_leadership']}\n"
        f"🏆 ציון פרופיל: {profile['profile_score']}"
    )
    await msg.answer(text, parse_mode="HTML")

@router.message(Command("xp"))
async def cmd_xp(msg: Message):
    await msg.answer("✅ מערכת XP פעילה. XP נצבר מפעולות כמו השלמת קורסים, הזמנת חברים, ניהול תקציב.")
