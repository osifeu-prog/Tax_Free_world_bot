from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.config import settings
from bot.database.session import engine
from datetime import datetime

router = Router()

start_time = datetime.now()

@router.message(Command("debug"))
async def cmd_debug(msg: Message):
    db_status = "🟢 מחובר" if engine else "🔴 לא מחובר"
    redis_status = "🟢 מחובר" if (await check_redis()) else "🔴 לא מחובר"
    uptime = datetime.now() - start_time
    text = (
        f"🔧 <b>סטטוס מערכת</b>\n"
        f"━━━━━━━━━━━━━━\n"
        f"⏱️ זמן פעילות: {uptime}\n"
        f"🗄️ מסד נתונים: {db_status}\n"
        f"📦 Redis: {redis_status}\n"
        f"🆔 Bot ID: {settings.bot_token[:10]}...\n"
    )
    await msg.answer(text, parse_mode="HTML")

async def check_redis():
    try:
        import os
        import redis.asyncio as redis
        r = redis.from_url(os.environ.get("REDIS_URL", "redis://localhost:6379"))
        await r.ping()
        return True
    except:
        return False
