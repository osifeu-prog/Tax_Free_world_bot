from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from bot.database.session import engine

router = Router()

ADMIN_IDS = [224223270, 8789977826]

@router.message(Command("admin_stats"))
async def admin_stats(msg: Message):
    if msg.from_user.id not in ADMIN_IDS:
        return await msg.answer("⛔ גישה מותרת רק למנהל.")
    async with engine.begin() as conn:
        total_users = (await conn.execute(text("SELECT COUNT(*) FROM users"))).scalar()
        total_expenses = (await conn.execute(text("SELECT COUNT(*) FROM user_expenses"))).scalar()
        total_donations = (await conn.execute(text("SELECT COUNT(*) FROM donations"))).scalar()
        total_points = (await conn.execute(text("SELECT SUM(points) FROM users"))).scalar() or 0
    txt = f"📊 <b>סטטיסטיקות מנהל</b>\n━━━━━━━━━━━━━━\n👥 משתמשים: {total_users}\n💰 הוצאות: {total_expenses}\n💖 תרומות: {total_donations}\n⭐ נקודות כולל: {total_points:,}"
    await msg.answer(txt, parse_mode="HTML")
