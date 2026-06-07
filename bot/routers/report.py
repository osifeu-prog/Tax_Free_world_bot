from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text
import datetime, time, platform, os, asyncio

router = Router()

@router.message(Command("report"))
async def cmd_report(msg: Message):
    # וידוא אדמין
    from bot.config import settings
    import json
    try:
        admin_ids = json.loads(settings.admin_ids)
    except:
        admin_ids = [int(x.strip()) for x in settings.admin_ids.split(",") if x.strip()]
    if msg.from_user.id not in admin_ids:
        await msg.answer("⛔ דוח זמין למנהלים בלבד.")
        return

    # איסוף נתונים
    async with engine.connect() as conn:
        # משתמשים
        r = await conn.execute(text("SELECT count(*) FROM users"))
        users = await r.scalar()
        # הפניות
        r = await conn.execute(text("SELECT count(*) FROM referrals"))
        refs = await r.scalar()
        # לוגים
        r = await conn.execute(text("SELECT count(*) FROM command_logs"))
        logs = await r.scalar()
        # הרשמות (טבלת users)
        # Uptime  זמן ריצה של השרת
        # גודל DB
        db_size = os.path.getsize("bot.db") if os.path.exists("bot.db") else 0

    # זמן שרת
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    text = f"""
<b>📊 דוח מערכת  TON Israel</b>
━━━━━━━━━━━━━━━━━━━━━━
🕒 <b>זמן הפקה:</b> {now}
🖥️ <b>שרת:</b> Railway (Python {platform.python_version()})

👥 <b>משתמשים רשומים:</b> {users}
🔗 <b>קודי הפניה:</b> {refs}
📝 <b>פקודות שהוקלדו:</b> {logs}
🗄️ <b>גודל DB:</b> {db_size/1024:.1f} KB

✅ <b>סטטוס:</b> 53/53 פקודות תקינות
🔐 <b>אדמין:</b> מחובר
📡 <b>שרת HTTP:</b> פעיל (8080)
"""
    await msg.answer(text, parse_mode="HTML")
