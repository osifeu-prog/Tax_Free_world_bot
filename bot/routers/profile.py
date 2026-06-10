from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text as sa_text
from bot.database.session import engine

router = Router()

def safe_format(value, default="—"):
    """המרה בטוחה של מספר לפורמט עם פסיקים, מחזירה default אם None"""
    return f"{value:,.0f}" if value is not None else default

@router.message(Command('profile'))
async def cmd_profile(msg: Message):
    uid = msg.from_user.id
    async with engine.begin() as conn:
        # פרטי משתמש בסיסיים
        user_result = await conn.execute(
            sa_text("SELECT language, points, wallet_address, created_at FROM users WHERE telegram_id=:uid"),
            {"uid": uid}
        )
        user = user_result.fetchone()

        # נתוני פנסיה (יכולים להיות None)
        pension_result = await conn.execute(
            sa_text("SELECT result_monthly, result_capital FROM pension_profiles WHERE telegram_id=:uid ORDER BY id DESC LIMIT 1"),
            {"uid": uid}
        )
        pension = pension_result.fetchone()

        total_users_result = await conn.execute(sa_text("SELECT COUNT(*) FROM users"))
        total_users = total_users_result.fetchone()[0]

    lang = user[0] if user else "he"
    points = user[1] if user else 0
    wallet = (user[2] or "לא הוגדר")[:12] if user else "לא הוגדר"
    created = str(user[3])[:10] if user and user[3] else "לא ידוע"

    txt = f"👤 <b>פרופיל  {msg.from_user.first_name}</b>\n━━━━━━━━━━━━━━━━━━\n🌐 שפה: {lang}\n⭐️ נקודות: {points}\n👛 ארנק: {wallet}...\n📅 הצטרף: {created}\n\n"
    
    if pension and (pension[0] is not None or pension[1] is not None):
        monthly = safe_format(pension[0])
        capital = safe_format(pension[1])
        txt += f"📊 <b>פנסיה</b>\n• חודשית: {monthly} \n• צבורה: {capital} \n\n"
    
    txt += f"🏙️ <b>TON City</b>\n• תושבים: {total_users}\n\n/pension | /donate | /setwallet"
    await msg.answer(txt, parse_mode='HTML')
