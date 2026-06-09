from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text

router = Router()

@router.message(Command("fix_users"))
async def cmd_fix_users(msg: Message):
    async with engine.begin() as conn:
        # בדוק אם העמודה קיימת
        cols = await conn.run_sync(lambda c: [row[1] for row in c.execute(text("PRAGMA table_info(users)")).fetchall()])
        if "referred_by" not in cols:
            await conn.run_sync(lambda c: c.execute(text("ALTER TABLE users ADD COLUMN referred_by INTEGER")))
            await msg.answer("✅ עמודת referred_by נוספה")
        else:
            await msg.answer("✅ העמודה already exists")
