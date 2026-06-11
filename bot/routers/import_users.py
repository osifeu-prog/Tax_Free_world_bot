from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from sqlalchemy import text

router = Router()

@router.message(Command("importusers"))
async def cmd_import(msg: Message):
    # פקודה למנהל בלבד  מייבאת users מ-JSON חיצוני
    try:
        import json
        with open("exports/users_backup.json", "r", encoding="utf-8") as f:
            users = json.load(f)
        async with async_session() as s:
            for user in users:
                await s.execute(
                    text("INSERT OR IGNORE INTO users (telegram_id, language, points) VALUES (:tid, :lang, :pts)"),
                    {"tid": user["telegram_id"], "lang": user.get("language", "he"), "pts": user.get("points", 0)}
                )
            await s.commit()
        await msg.answer(f"✅ יובאו {len(users)} משתמשים.")
    except Exception as e:
        await msg.answer(f"❌ שגיאה: {e}")
