from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text as sa_text
from bot.database.session import engine

router = Router()

@router.message(Command('stats_useless'))
async def cmd_stats_useless(msg: Message):
    async with engine.begin() as conn:
        users = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COUNT(*) FROM users")).fetchone()))[0]
        donations = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COUNT(*) FROM donations")).fetchone()))[0]
        amount = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COALESCE(SUM(amount), 0) FROM donations")).fetchone()))[0]
        ai_replies = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COUNT(*) FROM useless_log WHERE action='ai_reply'")).fetchone()))[0]
        roulette = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COUNT(*) FROM useless_log WHERE action='roulette_play'")).fetchone()))[0]
        red_buttons = (await conn.run_sync(lambda c: c.execute(sa_text("SELECT COUNT(*) FROM useless_log WHERE action='red_button_pressed'")).fetchone()))[0]
    txt = (
        "📊 <b>סטטיסטיקות חסרות תועלת</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"👥 משתמשים: {users}\n"
        f"💖 תרומות: {donations} ({amount})\n"
        f"🤖 AI replies: {ai_replies}\n"
        f"🎲 רולטות: {roulette}\n"
        f"🔴 כפתור אדום: {red_buttons}"
    )
    await msg.answer(txt, parse_mode='HTML')