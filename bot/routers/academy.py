from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("academy"))
async def cmd_academy(msg: Message):
    text = """
📚 <b>האקדמיה של TON Israel</b>
━━━━━━━━━━━━━━━━━━━━━━

ברוך הבא לקורסים ולתכנים החינוכיים שלנו!

<b>קורסים זמינים:</b>
• /crypto — מבוא לקריפטו וביטקוין
• /cbdc — CBDC והסכנות של מטבעות בנק מרכזי
• /decentral — ביזור מול ריכוז
• /socio — סוציוקרטיה ודמוקרטיה מבוזרת
• /anti — טכנולוגיות נגד שחיתות
• /edu — חינוך כלכלי ופיננסי
• /academy_extended — ביזוריות מתקדמת
• /academy_nft — NFT כזהות דיגיטלית
• /academy_dao — DAO וקהילות מבוזרות
• /vision — החזון המלא של TON Israel

🔗 בוט אקדמיה מתקדם: @SLH_Academia_bot
"""
    await msg.answer(text, parse_mode="HTML")
