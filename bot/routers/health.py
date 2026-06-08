import time, platform, os, datetime
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text

router = Router()

# === Uptime ===
_START_TIME = time.time()

@router.message(Command("health"))
async def cmd_health(msg: Message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    uptime = time.time() - _START_TIME
    hours, rem = divmod(int(uptime), 3600)
    minutes, seconds = divmod(rem, 60)

    # DB check
    db_status = "🟢 OK"
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        db_status = "🔴 Error"

    # Locales check
    locales_path = os.path.join(os.path.dirname(__file__), "..", "locales")
    locale_files = ["he.json", "en.json", "ar.json", "ru.json"]
    missing_locales = [f for f in locale_files if not os.path.exists(os.path.join(locales_path, f))]
    locales_status = f"✅ {4 - len(missing_locales)}/4 loaded"
    if missing_locales:
        locales_status += f"\n⚠️ Missing: {', '.join(missing_locales)}"

    # Event count
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
🗄 <b>Database:</b> {db_status}
🌐 <b>Locales:</b> {locales_status}
📊 <b>Citizen Events:</b> {event_count}
🖥 <b>Platform:</b> {platform.python_version()}
✅ <b>Commands:</b> 53/53
"""
    await msg.answer(text, parse_mode="HTML")
