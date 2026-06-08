from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("help"))
async def cmd_help(msg: Message):
    text = """
📖 <b>כל הפקודות  TON Israel</b>
━━━━━━━━━━━━━━━━━━━━━━
💰 <b>חיסכון אישי</b>
/start /compare /wallet /why /business /budget /profile /expenses /addexpense /setincome /delexpense
🏠 <b>משק בית</b>
/household /shopping /chore /familygroup
📚 <b>אקדמיה</b>
/crypto /cbdc /decentral /socio /anti /edu /academy_extended /academy_nft /academy_dao /vision /spark /academia
👥 <b>קהילה</b>
/ref /qr /stats /top /tip /contact /faq /daily /mydata /gift
🛠️ <b>כלים</b>
/miniapp /keyboard /hide /ask /feedback /help /quiz /menu /language
🔐 <b>הרשאות</b>
/requestadmin /addadmin /login /setpassword /removeadmin
🔒 <b>אדמין</b>
/admin /export /debug /addgroup /groups /report /setrole /seed_courses
👤 <b>הפרופיל שלי</b>
/myrole /mydata /setwallet
📊 <b>פנסיה</b>
/pension
💖 <b>תרומה</b>
/donate
"""
    await msg.answer(text, parse_mode="HTML")
