from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text
from datetime import datetime
import random

router = Router()

@router.message(Command("city"))
async def cmd_city(msg: Message):
    async with engine.connect() as conn:
        users = await conn.scalar(text("SELECT count(*) FROM users"))
        pensions = await conn.scalar(text("SELECT count(*) FROM pension_profiles"))
        courses = await conn.scalar(text("SELECT count(*) FROM courses"))
        # households table check
        households = 0
        try:
            households = await conn.scalar(text("SELECT count(*) FROM households"))
        except:
            pass
        donations = random.randint(0, 5)
    # Market index simulation
    base = 100
    sentiment = random.uniform(-3, 3)
    index = base + sentiment
    arrow = "↑" if sentiment > 0 else "↓" if sentiment < 0 else "→"
    now = datetime.now().strftime("%H:%M:%S")
    txt = (
        f"🏙️ <b>TON City Report</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🕒 זמן עיר: {now}\n"
        f"👥 תושבים: {users}\n"
        f"🏦 חשבונות פנסיה: {pensions}\n"
        f"🏠 משקי בית: {households}\n"
        f"🎓 קורסים: {courses}\n"
        f"💖 תרומות: {donations} TON\n"
        f"📈 בורסת TON City: {index:.1f} ({arrow}{abs(sentiment):.1f}%)\n"
    )
    await msg.answer(txt, parse_mode="HTML")
