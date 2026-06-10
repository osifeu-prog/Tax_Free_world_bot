from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from bot.database.session import engine

router = Router()

@router.message(Command("addcategory"))
async def add_category(msg: Message):
    parts = msg.text.split()
    if len(parts) < 3:
        await msg.answer("❗ שימוש: /addcategory type name   (type = expense/income)\nלדוגמה: /addcategory expense אוכל")
        return
    type_ = parts[1].lower()
    name = parts[2]
    uid = msg.from_user.id
    async with engine.begin() as conn:
        await conn.execute(
            text("INSERT INTO categories (user_id, name, type) VALUES (:uid, :name, :type)"),
            {"uid": uid, "name": name, "type": type_}
        )
    await msg.answer(f"✅ נוספה קטגוריית {type_}: {name}")

@router.message(Command("categories"))
async def list_categories(msg: Message):
    uid = msg.from_user.id
    async with engine.begin() as conn:
        res = await conn.execute(
            text("SELECT type, name FROM categories WHERE user_id = :uid ORDER BY type, name"),
            {"uid": uid}
        )
        rows = res.fetchall()
    exp = [r[1] for r in rows if r[0] == "expense"]
    inc = [r[1] for r in rows if r[0] == "income"]
    txt = "📂 <b>הקטגוריות שלך</b>\n"
    txt += f"💸 הוצאות: {', '.join(exp) if exp else 'אין'}\n"
    txt += f"💰 הכנסות: {', '.join(inc) if inc else 'אין'}\n"
    txt += "\nלהוספה: /addcategory expense שם"
    await msg.answer(txt, parse_mode="HTML")
