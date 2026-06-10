from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text as sa_text
from bot.database.session import engine

router = Router()

@router.message(Command('profile'))
async def cmd_profile(msg: Message):
    uid = msg.from_user.id
    async with engine.begin() as conn:
        user = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT language, points, wallet_address, created_at FROM users WHERE telegram_id=:uid"), {"uid": uid}).fetchone()))
        pension = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT result_monthly, result_capital FROM pension_profiles WHERE telegram_id=:uid ORDER BY id DESC LIMIT 1"), {"uid": uid}).fetchone()))
        total_users = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COUNT(*) FROM users")).fetchone()))[0]
        donations = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COUNT(*), COALESCE(SUM(amount),0) FROM donations WHERE user_id=:uid"), {"uid": uid}).fetchone()))

    lang = user[0] if user else "he"
    points = user[1] if user else 0
    wallet = (user[2] or "לא הוגדר")[:12]
    created = (user[3] or "לא ידוע")[:10]

    txt = (
        f"👤 <b>פרופיל  {msg.from_user.first_name}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🌐 שפה: {lang}\n⭐️ נקודות: {points}\n"
        f"👛 ארנק: {wallet}...\n📅 הצטרף: {created}\n\n"
    )
    if pension:
        txt += f"📊 <b>פנסיה</b>\n• חודשית: {pension[0]:,.0f} \n• צבורה: {pension[1]:,.0f} \n\n"
    txt += (
        f"💖 <b>תרומות</b>\n• {donations[0]} תרומות\n• סה\"כ: {donations[1]:,.0f} TON\n\n"
        f"🏙️ <b>TON City</b>\n• תושבים: {total_users}\n\n"
        f"/pension | /donate | /setwallet"
    )
    await msg.answer(txt, parse_mode='HTML')