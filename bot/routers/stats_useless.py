from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from bot.database.session import engine

router = Router()

@router.message(Command('stats_useless'))
async def cmd_stats_useless(msg: Message):
    async with engine.begin() as conn:
        total_users = await conn.run_sync(lambda c: c.execute(text("SELECT COUNT(*) FROM users")).fetchone()[0])
        pressed = await conn.run_sync(lambda c: c.execute(text("SELECT COUNT(DISTINCT user_id) FROM useless_log WHERE action='red_button_pressed'")).fetchone()[0])
        roulette_plays = await conn.run_sync(lambda c: c.execute(text("SELECT COUNT(*) FROM useless_log WHERE action='roulette_play'")).fetchone()[0])
    text_msg = (
        f"📊 <b>סטטיסטיקות חסרות תועלת</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👥 סה\"כ משתמשים: {total_users}\n"
        f"🔴 לחצו על הכפתור האדום: {pressed}\n"
        f"🎲 שיחקו ברולטה: {roulette_plays}\n"
        f"📉 אחוז לחיצה: {round(pressed/total_users*100,1) if total_users else 0}%\n\n"
        f"🤷♂️ כמעט כולם הבינו שאין טעם."
    )
    await msg.answer(text_msg, parse_mode='HTML')
