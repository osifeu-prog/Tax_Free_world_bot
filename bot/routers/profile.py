from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from bot.database.session import engine

router = Router()

def safe_format(value, default="—"):
    return f"{value:,.0f}" if value is not None else default

@router.message(Command('profile'))
async def cmd_profile(msg: Message):
    uid = msg.from_user.id
    async with engine.begin() as conn:
        user_result = await conn.execute(
            text("SELECT language, points, wallet_address, created_at FROM users WHERE telegram_id=:uid"),
            {"uid": uid}
        )
        user = user_result.fetchone()
        pension_result = await conn.execute(
            text("SELECT result_monthly, result_capital FROM pension_profiles WHERE telegram_id=:uid ORDER BY id DESC LIMIT 1"),
            {"uid": uid}
        )
        pension = pension_result.fetchone()
        total_result = await conn.execute(text("SELECT COUNT(*) FROM users"))
        total_users = total_result.scalar()

    lang = user[0] if user else "he"
    points = user[1] if user else 0
    wallet = (user[2] or "לא הוגדר")[:12] if user else "לא הוגדר"
    created = str(user[3])[:10] if user and user[3] else "לא ידוע"

    txt = f"👤 <b>פרופיל {msg.from_user.first_name}</b>\n━━━━━━━━━━━━━━\n🌐 שפה: {lang}\n⭐️ נקודות: {points}\n👛 ארנק: {wallet}...\n📅 הצטרף: {created}\n\n"
    if pension and (pension[0] or pension[1]):
        txt += f"📊 <b>פנסיה</b>\n• חודשית: {safe_format(pension[0])} \n• צבורה: {safe_format(pension[1])} \n\n"
    txt += f"🏙️ <b>TON City</b>\n• תושבים: {total_users}\n\n/pension | /donate | /setwallet"
    await msg.answer(txt)

