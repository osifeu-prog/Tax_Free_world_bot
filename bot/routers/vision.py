from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("vision"))
async def cmd_vision(msg: Message):
    text = """
🌐 <b>החזון של TON Israel</b>

אנחנו בונים פלטפורמה חינוכית-כלכלית מבוזרת:
• 🎓 <b>אקדמיה</b>  קורסים על ביזוריות, כלכלה חכמה, DAO, NFT.
• 🕹️ <b>משחקים</b>  "העיר המבוזרת", "צייד השחיתות", סימולציות.
• 🧑🤝🧑 <b>קהילה</b>  ניהול קבוצות, משק בית משותף, לוחות מובילים.
• 💎 <b>NFT-זהות</b>  כרטיס ביקור דיגיטלי, רישיון מקצועי.
• 🪙 <b>טוקן קהילתי</b>  תגמולים, Premium, כלכלה פנימית.

🔗 <b>האקדמיה שלנו:</b> @SLH_Spark_AI_BOT  
🔗 <b>תכנים מתקדמים:</b> @SLH_Academia_bot  

📌 <b>מתחילים עכשיו:</b> /academy  לבחירת מסלול למידה  
📌 <b>מנהלים:</b> /setrole  להגדיר תפקידים
"""
    await msg.answer(text, parse_mode="HTML")

@router.message(Command("spark"))
async def cmd_spark(msg: Message):
    await msg.answer("🤖 @SLH_Spark_AI_BOT  בוט הבינה המתקדם של הרשת.\nשאלו אותו כל דבר!")

@router.message(Command("academia"))
async def cmd_academia(msg: Message):
    await msg.answer("📚 @SLH_Academia_bot  תוכן אקדמי מורחב, קורסים ומשחקים.")
