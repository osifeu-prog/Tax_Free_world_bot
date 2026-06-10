from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from bot.database.session import engine
from datetime import datetime, timezone
import json

router = Router()

async def add_xp(user_id: int, xp_gain: int):
    async with engine.begin() as conn:
        # עדכון XP
        await conn.execute(text("UPDATE users SET xp = xp + :xp WHERE telegram_id = :uid"), {"xp": xp_gain, "uid": user_id})
        # בדיקת עליית רמה (נוסחה פשוטה: level = floor( (xp / 100) ^ 0.5 ) + 1)
        res = await conn.execute(text("SELECT xp FROM users WHERE telegram_id = :uid"), {"uid": user_id})
        xp = res.scalar()
        level = int((xp / 100) ** 0.5) + 1
        await conn.execute(text("UPDATE users SET level = :lvl WHERE telegram_id = :uid"), {"lvl": level, "uid": user_id})
        # עדכון streak (אם היה פעיל היום)
        today = datetime.now(timezone.utc).date()
        last_active_res = await conn.execute(text("SELECT last_active FROM users WHERE telegram_id = :uid"), {"uid": user_id})
        last_active = last_active_res.scalar()
        if last_active:
            last_date = last_active.date()
            if (today - last_date).days == 1:
                await conn.execute(text("UPDATE users SET streak_days = streak_days + 1 WHERE telegram_id = :uid"), {"uid": user_id})
            elif (today - last_date).days > 1:
                await conn.execute(text("UPDATE users SET streak_days = 1 WHERE telegram_id = :uid"), {"uid": user_id})
        else:
            await conn.execute(text("UPDATE users SET streak_days = 1 WHERE telegram_id = :uid"), {"uid": user_id})
        await conn.execute(text("UPDATE users SET last_active = :now WHERE telegram_id = :uid"), {"now": datetime.now(timezone.utc), "uid": user_id})
@router.message(Command("stats"))
async def show_stats(msg: Message):
    uid = msg.from_user.id
    async with engine.begin() as conn:
        res = await conn.execute(text("SELECT xp, level, streak_days FROM users WHERE telegram_id = :uid"), {"uid": uid})
        row = res.fetchone()
        if row:
            await msg.answer(f"🏆 <b>הסטטיסטיקות שלך</b>\n⭐ XP: {row[0]}\n📈 רמה: {row[1]}\n🔥 רצף יומי: {row[2]}", parse_mode="HTML")
        else:
            await msg.answer("לא נמצאו נתונים.")
