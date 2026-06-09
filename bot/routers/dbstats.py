from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text

router = Router()

@router.message(Command("dbstats"))
async def cmd_dbstats(msg: Message):
    async with engine.connect() as conn:
        tables = await conn.run_sync(lambda c: c.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall())
        table_list = ", ".join([row[0] for row in tables])
        user_count = await conn.scalar(text("SELECT count(*) FROM users")) or 0
        events_count = await conn.scalar(text("SELECT count(*) FROM events_log")) or 0
    await msg.answer(
        f"🗄️ <b>מצב מסד נתונים</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"📋 טבלאות: {table_list}\n"
        f"👥 משתמשים: {user_count}\n"
        f"📊 אירועים: {events_count}\n"
        f"💾 Volume: /app/bot/database/data\n"
        f"🟢 סטטוס: מחובר ופעיל",
        parse_mode="HTML"
    )
