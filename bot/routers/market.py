from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime
from zoneinfo import ZoneInfo
import random, math

router = Router()

@router.message(Command("market"))
async def cmd_market(msg: Message):
    now = datetime.now(ZoneInfo("Asia/Jerusalem")).strftime("%H:%M:%S")
    supply = random.uniform(80, 120)
    demand = random.uniform(80, 120)
    price = 100 * (demand / supply)
    change = price - 100
    arrow = "📈" if change > 0 else "📉" if change < 0 else "📊"
    text = (
        f"📊 <b>בורסת TON City</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🕒 שעון אמת: {now}\n"
        f"📦 היצע: {supply:.1f}\n"
        f"🛒 ביקוש: {demand:.1f}\n"
        f"💰 מחיר TONC: {price:.2f} {arrow}\n"
    )
    await msg.answer(text, parse_mode="HTML")
