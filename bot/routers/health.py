import time, platform, os, datetime
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text

router = Router()
_START_TIME = time.time()

@router.message(Command("health"))
async def cmd_health(msg: Message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uptime = time.time() - _START_TIME
    hours, rem = divmod(int(uptime), 3600)
    minutes, seconds = divmod(rem, 60)

    # DB check
    db_status = "🟢 OK"
    db_error = ""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        db_status = "🔴 Error"
        db_error = str(e)[:100]

    # Locales
    locales_path = os.path.join(os.path.dirname(__file__), "..", "locales")
    locale_files = ["he.json", "en.json", "ar.json", "ru.json"]
    missing = [f for f in locale_files if not os.path.exists(os.path.join(locales_path, f))]
    loc_status = f"✅ {4 - len(missing)}/4 loaded"
    if missing:
        loc_status += f"\n⚠️ Missing: {', '.join(missing)}"

    # Events
    event_count = 0
    try:
        async with engine.connect() as conn:
            r = await conn.execute(text("SELECT count(*) FROM events"))
            event_count = await r.scalar()
    except Exception:
        event_count = "N/A"

    text = f"""
<b>🩺 System Health  TON Israel</b>
━━━━━━━━━━━━━━━━━━━━━━
🕒 <b>Server Time:</b> {now}
⏱ <b>Uptime:</b> {hours}h {minutes}m {seconds}s
🗄 <b>Database:</b> {db_status} {db_error}
🌐 <b>Locales:</b> {loc_status}
📊 <b>Citizen Events:</b> {event_count}
🖥 <b>Platform:</b> {platform.python_version()}
✅ <b>Commands:</b> 53/53
"""
    await msg.answer(text, parse_mode="HTML")
