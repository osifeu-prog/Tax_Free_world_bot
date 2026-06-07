from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from bot.config import settings
from bot.services.export_service import export_logs_csv
import os

router = Router()

@router.message(Command("admin"))
async def cmd_admin(msg: Message):
    if msg.from_user.id not in settings.admin_ids:
        await msg.answer("⛔ אין לך הרשאות גישה לאזור זה.")
        return
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 ייצוא לוגים", callback_data="export_csv")],
        [InlineKeyboardButton(text="📈 סטטיסטיקות", callback_data="stats")],
        [InlineKeyboardButton(text="🔄 רענון", callback_data="start")],
    ])
    await msg.answer("🔐 <b>אזור אדמין</b>", parse_mode="HTML", reply_markup=kb)

@router.callback_query(F.data == "export_csv")
async def handle_export(call: CallbackQuery):
    if call.from_user.id not in settings.admin_ids:
        await call.answer("⛔ אין הרשאה", show_alert=True)
        return
    await call.message.answer("📊 מייצא נתונים...")
    csv_data = await export_logs_csv()
    os.makedirs("exports", exist_ok=True)
    file_path = "exports/logs.csv"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(csv_data)
    await call.message.answer_document(FSInputFile(file_path), caption="📋 ייצוא לוגים (1000 אחרונים)")
    await call.answer()
