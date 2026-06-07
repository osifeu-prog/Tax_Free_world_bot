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
/start  דף הבית
/compare  מחשבון עמלות
/wallet  ארנק TON
/budget  תקציב
/profile  פרופיל
/expenses  הוצאות
/addexpense  הוסף הוצאה
/setincome  עדכן הכנסה
/delexpense  מחק הוצאה

━━━━━━━━━━━━━━━━━━━━━━
🏠 <b>משק בית</b>
/household  ניהול משק בית

━━━━━━━━━━━━━━━━━━━━━━
📚 <b>אקדמיה</b>
/crypto  קריפטו
/cbdc  CBDC
/decentral  ביזור
/socio  סוציוקרטיה
/anti  נגד שחיתות
/edu  חינוך
/academy_extended  ביזוריות, NFT
/academy_nft  NFT-זהות
/academy_dao  DAO
/vision  החזון המלא
/spark  @SLH_Spark_AI_BOT
/academia  @SLH_Academia_bot

━━━━━━━━━━━━━━━━━━━━━━
👥 <b>קהילה</b>
/ref  הפניה
/qr  QR אישי
/stats  סטטיסטיקות
/top  מובילים
/tip  טיפ יומי
/contact  צור קשר
/faq  שאלות נפוצות
/daily  סיכום יומי
/mydata  הנתונים שלי
/gift  מתנה יומית

━━━━━━━━━━━━━━━━━━━━━━
🛠️ <b>כלים</b>
/miniapp  מחשבון ויזואלי
/keyboard  מקלדת
/hide  הסתר מקלדת
/ask  שאל את הבינה
/feedback  דיווח
/help  עזרה
/quiz  חידון

━━━━━━━━━━━━━━━━━━━━━━
🔐 <b>הרשאות</b>
/requestadmin  בקש הרשאות
/addadmin  הוסף מנהל (אדמין)
/removeadmin  הסר מנהל (אדמין)
/setpassword  שנה סיסמה (אדמין)

━━━━━━━━━━━━━━━━━━━━━━
🔒 <b>ניהול (אדמינים)</b>\n/report  דוח מלא
/admin  לוח בקרה
/export  ייצוא
/debug  סטטוס
/addgroup  הוסף קבוצה
/groups  רשימת קבוצות
"""
    await msg.answer(text, parse_mode="HTML")

