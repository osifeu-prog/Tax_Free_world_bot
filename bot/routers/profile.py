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
        # User basics
        user = await conn.execute(
            sa_text("SELECT language, points, wallet_address, created_at FROM users WHERE telegram_id=:uid"), 
            {"uid": uid}
        ).fetchone()

        # Pension
        pension = await conn.execute(
            sa_text("SELECT result_monthly, result_capital FROM pension_profiles WHERE telegram_id=:uid ORDER BY id DESC LIMIT 1"), 
            {"uid": uid}
        ).fetchone()

        total_users = (await conn.execute(sa_text("SELECT COUNT(*) FROM users")).fetchone())[0]

    lang = user[0] if user else "he"
    points = user[1] if user else 0
    wallet = (user[2] or "לא הוגדר")[:12] if user and user[2] else "לא הוגדר"
    created = str(user[3])[:10] if user and user[3] else "חדש"

    txt = f"👤 <b>פרופיל {msg.from_user.first_name}</b>\n\n"
    txt += f"🌐 שפה: {lang}\n💎 נקודות: {points}\n👛 ארנק: {wallet}...\n📅 הצטרף: {created}\n\n"

    if pension:
        txt += f"📊 פנסיה חודשית: {pension[0]:,.0f} \n💰 הון פנסיוני: {pension[1]:,.0f} \n\n"

    txt += f"🏙️ TON City: {total_users} תושבים\n\n"
    txt += "/pension | /donate | /setwallet"

    await msg.answer(txt, parse_mode='HTML')
