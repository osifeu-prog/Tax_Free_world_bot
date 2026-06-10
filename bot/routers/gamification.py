from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from bot.database.session import engine, async_session
from bot.database.models import User
import random, datetime

router = Router()

@router.message(Command('daily'))
async def cmd_daily(msg: Message):
    uid = msg.from_user.id
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        if not u:
            await msg.answer("תחילה שלח /start")
            return
        points = getattr(u, 'points', 0) or 0
        u.points = points + random.randint(1, 10)
        await s.commit()
        await msg.answer(f"🎮 <b>סטריק יומי!</b>\n\nהרווחת {u.points - points} נקודות חסרות תועלת.\nסה\"כ: {u.points} נקודות.\n\n🤷♂️ אפשר להשתמש בהן לכלום.")

@router.message(Command('top'))
async def cmd_top(msg: Message):
    async with engine.begin() as conn:
        rows = await conn.run_sync(lambda c: c.execute(text("SELECT telegram_id, points FROM users ORDER BY points DESC LIMIT 10")).fetchall())
    text = "🏆 <b>לוח מובילים  חסרי תועלת</b>\n━━━━━━━━━━━━━━━━\n"
    for i, row in enumerate(rows, 1):
        text += f"{i}. {row[0]}  {row[1]} נק'\n"
    text += "\n💡 רוצה לעלות? שתף עם חברים."
    await msg.answer(text, parse_mode='HTML')

@router.message(Command('ref'))
async def cmd_ref(msg: Message):
    uid = msg.from_user.id
    ref_link = f"https://t.me/Tax_Free_world_bot?start=ref{uid}"
    async with engine.begin() as conn:
        count = await conn.run_sync(lambda c: c.execute(text("SELECT COUNT(*) FROM users WHERE referred_by=:uid"), {"uid": uid}).fetchone()[0])
    await msg.answer(
        f"🔗 <b>הקוד האישי שלך</b>\n\n"
        f"{ref_link}\n\n"
        f"👥 הצטרפו דרכך: {count} חסרי תועלת\n"
        f"💡 שתף עם חברים  ממילא אין לך מה להפסיד.",
        parse_mode='HTML'
    )