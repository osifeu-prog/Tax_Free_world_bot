import asyncio, time, datetime
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text
import json

router = Router()

@router.message(Command("report"))
async def cmd_report(msg: Message):
    from bot.config import settings
    try:
        admin_ids = json.loads(settings.admin_ids)
    except:
        admin_ids = [int(x.strip()) for x in (settings.admin_ids or "").split(",") if x.strip()]
    if admin_ids and msg.from_user.id not in admin_ids:
        await msg.answer("⛔ פקודת אדמין בלבד.")
        return

    out_text = "📊 דוח לא זמין כרגע"
    try:
        async with engine.connect() as conn:
            users = await conn.scalar(text("SELECT count(*) FROM users"))
            refs = await conn.scalar(text("SELECT count(*) FROM referrals"))
            logs = await conn.scalar(text("SELECT count(*) FROM command_logs"))
            try:
                events = await conn.scalar(text("SELECT count(*) FROM events"))
            except:
                events = "N/A"

        uptime_seconds = int(time.time() - start_time) if 'start_time' in globals() else 0
        hours, rem = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        out_text = f"""<b>📊 דוח מערכת  TON Israel</b>
━━━━━━━━━━━━━━━━━━━━━━
🕒 <b>זמן:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
⏱ <b>Up:</b> {hours}h {minutes}m {seconds}s
👥 <b>משתמשים:</b> {users}
🔗 <b>הפניות:</b> {refs}
📝 <b>לוגים:</b> {logs}
📊 <b>אירועים:</b> {events}
"""
    except Exception as e:
        out_text = f"📊 דוח מערכת  שגיאה: {e}"

    await msg.answer(out_text, parse_mode="HTML")
