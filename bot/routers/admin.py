from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from bot.database.session import engine

router = Router()
ADMIN_ID = 224223270  # החלף למזהה שלך

@router.message(Command("stats"))
async def cmd_stats(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await msg.answer("⛔ גישה מותרת רק למנהל.")
        return
    async with engine.begin() as conn:
        total_users = (await conn.execute(text("SELECT COUNT(*) FROM users"))).scalar() or 0
        total_donations = (await conn.execute(text("SELECT COALESCE(SUM(amount),0) FROM donations"))).scalar()
        # פשוט  בלי user_logs כרגע
    await msg.answer(
        f"📊 <b>סטטיסטיקות הבוט</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👥 סה\"כ משתמשים: {total_users}\n"
        f"💰 סך תרומות: {total_donations:,.0f} \n"
        f"🎰 Slots  (יוטמע בהמשך)",
        parse_mode="HTML"
    )