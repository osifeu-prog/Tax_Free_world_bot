from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("menu"))
async def cmd_menu(msg: Message):
    text = """
<b>📋 תפריט ראשי  TON Israel</b>
━━━━━━━━━━━━━━━━━━━━━━
💰 <b>חיסכון אישי</b>
/start /compare /wallet /why /business /budget /profile /expenses /addexpense /setincome /delexpense

🏠 <b>משק בית</b>
/household /shopping /chore

📚 <b>אקדמיה</b>
/academy /crypto /cbdc /decentral /socio /anti /edu /academy_extended /academy_nft /academy_dao /vision /spark

👥 <b>קהילה</b>
/ref /qr /stats /top /tip /contact /faq /daily /mydata /gift

🛠️ <b>כלים</b>
/miniapp /keyboard /hide /ask /feedback /help /quiz /id /ai /architecture

🔐 <b>הרשאות</b>
/requestadmin /addadmin /login /setpassword /removeadmin

🔒 <b>ניהול (אדמין)</b>
/admin /export /debug /addgroup /groups /report /setrole

👤 <b>הפרופיל שלי</b>
/myrole /mydata
"""
    await msg.answer(text, parse_mode="HTML")
