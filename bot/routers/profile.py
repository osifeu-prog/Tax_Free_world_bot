from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text as sa_text
from bot.database.session import engine, async_session
from bot.database.models import User
from sqlalchemy import select

router = Router()

@router.message(Command('profile'))
async def cmd_profile(msg: Message):
    uid = msg.from_user.id
    async with engine.begin() as conn:
        # User basics
        user = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT language, points, wallet_address, created_at FROM users WHERE telegram_id=:uid"), {"uid": uid}).fetchone()))
        # Income/expenses
        income = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COALESCE(SUM(amount),0) FROM user_expenses WHERE user_id=:uid AND type='income'"), {"uid": uid}).fetchone()))[0]
        expenses = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COALESCE(SUM(amount),0) FROM user_expenses WHERE user_id=:uid AND type='expense'"), {"uid": uid}).fetchone()))[0]
        # Pension
        pension = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT result_monthly, result_capital FROM pension_profiles WHERE telegram_id=:uid ORDER BY id DESC LIMIT 1"), {"uid": uid}).fetchone()))
        # TON City
        city = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COUNT(*) FROM users")).fetchone()))[0]
        # Courses
        courses = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COUNT(*) FROM user_progress WHERE user_id=:uid"), {"uid": uid}).fetchone()))[0]
        # Donations
        donations = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COUNT(*), COALESCE(SUM(amount),0) FROM donations WHERE user_id=:uid"), {"uid": uid}).fetchone()))
        # Household
        household = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT household_id, role FROM household_members WHERE user_id=:uid LIMIT 1"), {"uid": uid}).fetchone()))

    lang = user[0] if user else "he"
    points = user[1] if user else 0
    wallet = user[2] if user else "לא הוגדר"
    created = user[3] if user else "לא ידוע"

    txt = (
        f"👤 <b>פרופיל  {msg.from_user.first_name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🌐 שפה: {lang}\n"
        f"⭐️ נקודות: {points}\n"
        f"👛 ארנק: {wallet[:10]}...\n"
        f"📅 הצטרף: {created[:10]}\n\n"
        f"💰 <b>כלכלה</b>\n"
        f"• הכנסה: {income:,.0f} \n"
        f"• הוצאות: {expenses:,.0f} \n"
        f"• חיסכון: {income - expenses:,.0f} \n\n"
    )
    if pension:
        txt += f"📊 <b>פנסיה</b>\n• חודשית: {pension[0]:,.0f} \n• צבורה: {pension[1]:,.0f} \n\n"
    if household:
        txt += f"🏠 <b>משק בית</b>\n• קבוצה #{household[0]}\n• תפקיד: {household[1]}\n\n"
    txt += (
        f"🎓 <b>קורסים</b>\n• {courses} קורסים בתהליך\n\n"
        f"💖 <b>תרומות</b>\n• {donations[0]} תרומות\n• סה\"כ: {donations[1]:,.0f} TON\n\n"
        f"🏙️ <b>TON City</b>\n• תושבים: {city}\n\n"
        f"/setincome | /addexpense | /pension | /donate"
    )
    await msg.answer(txt, parse_mode='HTML')