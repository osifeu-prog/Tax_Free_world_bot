from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text

router = Router()

@router.message(Command("init_donations"))
async def cmd_init_donations(msg: Message):
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: c.execute(text("""
            CREATE TABLE IF NOT EXISTS donations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                tx_hash TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)))
    await msg.answer("✅ טבלת donations נוצרה")
