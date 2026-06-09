from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text

router = Router()

@router.message(Command("init_indexes"))
async def cmd_init_indexes(msg: Message):
    async with engine.begin() as conn:
        queries = [
            "CREATE INDEX IF NOT EXISTS idx_users_language ON users(language)",
            "CREATE INDEX IF NOT EXISTS idx_users_referred_by ON users(referred_by)",
            "CREATE INDEX IF NOT EXISTS idx_pension_profiles_user ON pension_profiles(telegram_id)",
            "CREATE INDEX IF NOT EXISTS idx_events_log_user ON events_log(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_events_log_type ON events_log(event_type)",
            "CREATE INDEX IF NOT EXISTS idx_events_log_timestamp ON events_log(timestamp)",
        ]
        for q in queries:
            try:
                await conn.run_sync(lambda c: c.execute(text(q)))
            except Exception as e:
                if "no such column" in str(e):
                    pass  # ignore missing column, will be created by create_all
                else:
                    raise
    await msg.answer("✅ אינדקסים נוצרו (או דולגו אם חסרה עמודה)")
