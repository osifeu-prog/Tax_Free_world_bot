from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy import text
from bot.database.session import engine
import logging

router = Router()
logger = logging.getLogger(__name__)

async def get_categories(user_id, type_):
    async with engine.begin() as conn:
        res = await conn.execute(
            text("SELECT name FROM categories WHERE user_id = :uid AND type = :type ORDER BY name"),
            {"uid": user_id, "type": type_}
        )
        return [row[0] for row in res.fetchall()]

@router.message(Command("addexpense"))
async def add_expense_start(msg: Message):
    uid = msg.from_user.id
    cats = await get_categories(uid, "expense")
    if not cats:
        cats = ["מזון", "תחבורה", "בידור", "קניות", "חשבונות", "אחר"]
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=c)] for c in cats], resize_keyboard=True)
    await msg.answer
    await add_xp(uid, 10)("📝 באיזו קטגוריה? (לחץ/י על כפתור)", reply_markup=kb)
    # נשתמש ב-FSM פשוט: נסמן בתגובה הבאה את הקטגוריה
    # נשתמש במשתנה זמני  נחזור על ה-state.

# FSM פשוט: נשתמש במטמון זיכרון  כאן נבצע קריאה ישירה במעטפת
# במקום FSM מורכב, נבקש גם סכום וגם קטגוריה באותו שלב? נפריד לשלושה שלבים.
# לצורך פשטות, נבצע דרך הודעות טקסט עם שאלות.

# נשתמש בהקלדה: /addexpense 50 מזון "אוכל"
# או לחלופין: שלב 2: לאחר הקטגוריה, מבקשים סכום.

# פיתרון מהיר: נשתמש בפקודה בשורה אחת:
@router.message(Command("adde"))
async def add_expense_quick(msg: Message):
    parts = msg.text.split()
    if len(parts) < 3:
        await msg.answer
    await add_xp(uid, 10)("❗ שימוש: /adde סכום קטגוריה [תיאור]\nלדוגמה: /adde 50 מזון ארוחת צהריים")
        return
    amount = float(parts[1])
    category = parts[2]
    description = " ".join(parts[3:]) if len(parts) > 3 else ""
    uid = msg.from_user.id
    async with engine.begin() as conn:
        await conn.execute(
            text("INSERT INTO expenses (user_id, amount, category, description) VALUES (:uid, :amt, :cat, :desc)"),
            {"uid": uid, "amt": amount, "cat": category, "desc": description}
        )
    await msg.answer
    await add_xp(uid, 10)(f"✅ נרשמה הוצאה: {amount}  בקטגוריית {category}")

# פקודה להצגת ההוצאות האחרונות
@router.message(Command("expenses"))
async def show_expenses(msg: Message):
    uid = msg.from_user.id
    async with engine.begin() as conn:
        res = await conn.execute(
            text("SELECT amount, category, description, created_at FROM expenses WHERE user_id = :uid ORDER BY created_at DESC LIMIT 10"),
            {"uid": uid}
        )
        rows = res.fetchall()
    if not rows:
        await msg.answer
    await add_xp(uid, 10)("📭 אין הוצאות עדיין. השתמש ב /adde")
        return
    txt = "📋 <b>10 ההוצאות האחרונות</b>\n"
    for r in rows:
        txt += f"💰 {r[0]}  | {r[1]} | {r[2][:20]}\n"
    await msg.answer
    await add_xp(uid, 10)(txt, parse_mode="HTML")

