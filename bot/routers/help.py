from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.keyboards.inline import back_to_main

router = Router()

HELP_TEXT = '''
📖 <b>כל הפקודות  TON Israel</b>

💰 <b>חיסכון:</b>
/start  דף הבית
/compare  מחשבון עמלות
/wallet  ארנק TON
/why  למה TON?
/business  לעסקים

🏠 <b>ניהול כלכלת הבית:</b>
/budget  מחשבון תקציב
/profile  פרופיל כלכלי
/addexpense  הוסף הוצאה
/expenses  צפה בהוצאות
/setincome  עדכן הכנסה
/delexpense  מחק הוצאה

📚 <b>אקדמיה:</b>
/crypto  קריפטו
/cbdc  CBDC
/decentral  ביזור מול ריכוזיות
/socio  סוציוקרטיה
/anti  טכנולוגיות נגד שחיתות
/edu  חינוך, כלכלה, רווחה
/academy_extended  ביזוריות, NFT, כלכלה חכמה
/academy_nft  NFT-זהות
/academy_dao  DAO

👥 <b>קהילה:</b>
/ref  קוד הפניה
/stats  סטטיסטיקות
/top  לוח מובילים
/tip  טיפ יומי
/contact  צור קשר
/id  זיהוי
/daily  סיכום יומי
/mydata  הנתונים שלי
/gift  מתנה יומית 🎰

🛠️ <b>כלים:</b>
/miniapp  מחשבון ויזואלי
/keyboard  מקלדת
/hide  הסתר מקלדת
/ask  שאל שאלה
/feedback  דיווח
/help  עזרה
/quiz  חידון

🔐 <b>הרשאות:</b>
/requestadmin  בקש הרשאת ניהול
/addadmin  הוסף מנהל
/login  התחבר
/setpassword  שנה סיסמה
/removeadmin  הסר מנהל

🔒 <b>אדמין (רק למנהלים):</b>
/admin  אזור אדמין
/export  ייצוא לוגים
/debug  סטטוס מערכת
'''

@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer(HELP_TEXT, parse_mode="HTML")

@router.callback_query(F.data == "help")
async def help_cb(call: CallbackQuery):
    await call.message.edit_text(HELP_TEXT, parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()
