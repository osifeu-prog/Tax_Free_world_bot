from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("familygroup"))
async def cmd_familygroup(msg: Message):
    # קישור ליצירת קבוצה חדשה
    import random, string
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    bot_username = "Tax_Free_world_bot"
    invite_link = f"https://t.me/{bot_username}?startgroup={code}"
    text = f"""
🏠 <b>יצירת קבוצה משפחתית</b>

1️⃣ <a href="{invite_link}">לחץ כאן</a> כדי ליצור קבוצה חדשה ולהוסיף את הבוט.
2️⃣ לאחר היצירה, שלח בקבוצה:
   <code>/household create</code>  כדי להתחיל לנהל את התקציב המשפחתי.

💡 <b>טיפ:</b> הוסף את בני המשפחה לקבוצה ושתף איתם את המשימות!
"""
    await msg.answer(text, parse_mode="HTML", disable_web_page_preview=True)
