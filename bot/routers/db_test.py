from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from bot.database.session import engine, async_session
from bot.database.models import User
import datetime

router = Router()

@router.message(Command("db_test"))
async def db_test(msg: Message):
    report = []
    async with engine.begin() as conn:
        # Tables
        tables = await conn.run_sync(lambda c: [row[0] for row in c.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()])
        report.append(f"🗃️ Tables: {', '.join(tables)}")
        # Users count
        count = await conn.run_sync(lambda c: c.execute(text("SELECT COUNT(*) FROM users")).fetchone()[0])
        report.append(f"👥 Users: {count}")
        # Add dummy
        await conn.run_sync(lambda c: c.execute(text("INSERT INTO users (telegram_id, language, role, created_at) VALUES (999999, 'he', 'test', :ts)"), {"ts": datetime.datetime.utcnow().isoformat()}))
        report.append("✅ Dummy user inserted")
        # Verify
        row = await conn.run_sync(lambda c: c.execute(text("SELECT telegram_id, language FROM users WHERE telegram_id=999999")).fetchone())
        report.append(f"🔍 Verified: {row}")
        # Clean
        await conn.run_sync(lambda c: c.execute(text("DELETE FROM users WHERE telegram_id=999999")))
        report.append("🧹 Dummy user deleted")
    await msg.answer("📊 <b>DB Test Report</b>\n" + "\n".join(report), parse_mode="HTML")
