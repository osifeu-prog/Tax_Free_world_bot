from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import json, os

router = Router()

PLAN_FILE = "work_plan.json"

@router.message(Command("loadplan"))
async def cmd_loadplan(msg: Message):
    if not os.path.exists(PLAN_FILE):
        await msg.answer("📭 אין תוכנית שמורה.")
        return
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    await msg.answer(f"📋 <b>תוכנית נוכחית:</b>\n{data['plan']}\n\n🕒 עודכן: {data['updated']}", parse_mode="HTML")
