from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text, Table, Column, Integer, String, MetaData, DateTime
from datetime import datetime

router = Router()

@router.message(Command("init_events"))
async def cmd_init_events(msg: Message):
    async with engine.begin() as conn:
        await conn.run_sync(lambda sync_conn: sync_conn.execute(text("""
            CREATE TABLE IF NOT EXISTS events_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                event_type TEXT,
                payload TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)))
    await msg.answer("✅ טבלת events_log נוצרה")
