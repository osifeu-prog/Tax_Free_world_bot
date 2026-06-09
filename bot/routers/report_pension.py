from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text

router = Router()

@router.message(Command("report_pension"))
async def cmd_report_pension(msg: Message):
    async with engine.connect() as conn:
        users = await conn.scalar(text("SELECT count(*) FROM pension_profiles"))
        avg_age = await conn.scalar(text("SELECT avg(age_now) FROM pension_profiles")) or 0
        avg_salary = await conn.scalar(text("SELECT avg(salary_bruto) FROM pension_profiles")) or 0
    await msg.answer(
        f"📊 <b>דוח פנסיה</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👥 משתמשים: {users}\n"
        f"🎂 גיל ממוצע: {avg_age:.1f}\n"
        f"💰 שכר ממוצע: {avg_salary:,.0f} שח",
        parse_mode="HTML"
    )
