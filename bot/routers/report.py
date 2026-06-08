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
            events = await conn.scalar(text("SELECT count(*) FROM events"))
            en = await conn.scalar(text("SELECT count(*) FROM users WHERE language='en'"))
            he = await conn.scalar(text("SELECT count(*) FROM users WHERE language='he'"))
            wallets = await conn.scalar(text("SELECT count(*) FROM users WHERE wallet_address IS NOT NULL"))

        out_text = f"""<b>📊 דוח מערכת  TON Israel</b>
━━━━━━━━━━━━━━━━━━━━━━
👥 <b>משתמשים:</b> {users}
🔗 <b>הפניות:</b> {refs}
📝 <b>לוגים:</b> {logs}
📊 <b>אירועים:</b> {events}
🌐 <b>אנגלית:</b> {en} | 🇮🇱 <b>עברית:</b> {he}
👛 <b>עם ארנק:</b> {wallets}
"""
    except Exception as e:
        out_text = f"📊 דוח מערכת  שגיאה: {e}"

    await msg.answer(out_text, parse_mode="HTML")
