from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import json, os, asyncio
from bot.routers.report import cmd_report

router = Router()

PLAN_FILE = "work_plan.json"

@router.message(Command("morning"))
async def cmd_morning(msg: Message):
    # 1. דו"ח מערכת
    await cmd_report(msg)
    # 2. תוכנית
    if os.path.exists(PLAN_FILE):
        with open(PLAN_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        await msg.answer(f"📋 <b>המשך מהתוכנית:</b>\n{data['plan']}", parse_mode="HTML")
    else:
        await msg.answer("📭 אין תוכנית. השתמש ב‑/saveplan כדי ליצור.")
    # 3. הצעת צעדים
    await msg.answer("💡 <b>צעדים מומלצים:</b>\n1. /smoke_test\n2. /pre_deploy_check\n3. /git_push", parse_mode="HTML")
