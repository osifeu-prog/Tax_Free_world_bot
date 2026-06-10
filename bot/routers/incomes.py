from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from bot.database.session import engine

router = Router()

@router.message(Command("addincome"))
async def add_income(msg: Message):
    parts = msg.text.split()
    if len(parts) < 2:
        await msg.answer("❗ שימוש: /addincome סכום [קטגוריה] [תיאור]")
        return
    amount = float(parts[1])
    category = parts[2] if len(parts) > 2 else "הכנסה"
    description = " ".join(parts[3:]) if len(parts) > 3 else ""
    uid = msg.from_user.id
    async with engine.begin() as conn:
        await conn.execute(
            text("INSERT INTO incomes (user_id, amount, category, description) VALUES (:uid, :amt, :cat, :desc)"),
            {"uid": uid, "amt": amount, "cat": category, "desc": description}
        )
    await msg.answer(f"✅ נרשמה הכנסה: {amount}  בקטגוריית {category}")

@router.message(Command("incomes"))
async def show_incomes(msg: Message):
    uid = msg.from_user.id
    async with engine.begin() as conn:
        res = await conn.execute(
            text("SELECT amount, category, description, created_at FROM incomes WHERE user_id = :uid ORDER BY created_at DESC LIMIT 10"),
            {"uid": uid}
        )
        rows = res.fetchall()
    if not rows:
        await msg.answer("📭 אין הכנסות עדיין.")
        return
    txt = "📋 <b>10 ההכנסות האחרונות</b>\n"
    for r in rows:
        txt += f"💵 {r[0]}  | {r[1]} | {r[2][:20]}\n"
    await msg.answer(txt, parse_mode="HTML")
