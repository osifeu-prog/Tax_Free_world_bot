from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import shutil, os, datetime

router = Router()

@router.message(Command("backup"))
async def cmd_backup(msg: Message):
    src = "/app/bot/database/data/bot.db"
    dst = f"/app/bot/database/data/backup_{datetime.date.today().isoformat()}.db"
    try:
        shutil.copy2(src, dst)
        await msg.answer(f"✅ גיבוי נוצר: {os.path.basename(dst)}")
    except Exception as e:
        await msg.answer(f"❌ שגיאת גיבוי: {e}")
