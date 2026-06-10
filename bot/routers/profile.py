from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text as sa_text
from bot.database.session import engine

router = Router()

async def ensure_donations_table():
    async with engine.begin() as conn:
        await conn.execute(sa_text('''
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        '''))

@router.message(Command('profile'))
async def cmd_profile(msg: Message):
    await ensure_donations_table()  # ✅ יוצר טבלה אם חסרה
    
    uid = msg.from_user.id
    async with engine.begin() as conn:
        user = await conn.execute(sa_text("SELECT language, points, wallet_address, created_at FROM users WHERE telegram_id=:uid"), {"uid": uid}).fetchone()
        pension = await conn.execute(sa_text("SELECT result_monthly, result_capital FROM pension_profiles WHERE telegram_id=:uid ORDER BY id DESC LIMIT 1"), {"uid": uid}).fetchone()
        total_users = (await conn.execute(sa_text("SELECT COUNT(*) FROM users")).fetchone())[0]

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
        f"🏙️ <b>TON City</b>\n• תושבים: {total_users}\n\n"
        f"/pension | /donate | /setwallet"
    )
    await msg.answer(txt, parse_mode='HTML')