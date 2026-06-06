from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from bot.config import settings
from bot.services.export_service import export_logs_csv
import os

router = Router()

@router.message(Command("export"))
async def cmd_export(msg: Message):
    if msg.from_user.id not in settings.admin_ids:
        await msg.answer("⛔ גישה למנהלים בלבד.")
        return
    await msg.answer("📊 מייצא נתונים...")
    csv_data = await export_logs_csv()
    os.makedirs("exports", exist_ok=True)
    file_path = "exports/logs.csv"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(csv_data)
    await msg.answer_document(FSInputFile(file_path), caption="📋 ייצוא לוגים (1000 אחרונים)")
