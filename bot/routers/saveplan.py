from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import json, os

router = Router()

PLAN_FILE = "work_plan.json"

@router.message(Command("saveplan"))
async def cmd_saveplan(msg: Message):
    plan = msg.text.replace("/saveplan", "").strip()
    if not plan:
        await msg.answer("השתמש: /saveplan <התוכנית שלך>")
        return
    with open(PLAN_FILE, "w", encoding="utf-8") as f:
        json.dump({"plan": plan, "updated": str(msg.date)}, f, ensure_ascii=False)
    await msg.answer("✅ תוכנית העבודה נשמרה.")
