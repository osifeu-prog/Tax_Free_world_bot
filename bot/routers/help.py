from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
router = Router()

@router.message(Command('help'))
async def cmd_help(msg: Message):
    text = (
        "<b>📖 עזרה  TON Israel</b>\n\n"
        "<b>💰 חיסכון</b>\n/start - 🚀 התחל\n/compare - 📊 השוואת עמלות\n/wallet - 👛 ארנק\n/why - ❓ למה TON\n/business - 💼 עסקים\n"
        "/budget - 💰 תקציב\n/profile - 👤 פרופיל\n/expenses - 📋 הוצאות\n/addexpense - ➕ הוסף הוצאה\n/setincome - 💵 קבע הכנסה\n"
        "/delexpense - 🗑️ מחק הוצאה\n/mysavings - 🐷 חיסכון שלי\n/setwallet - 🔑 הגדר ארנק\n\n"
        "<b>📊 פנסיה</b>\n/pension - 📊 פנסיה\n/report_pension - 📈 דוח פנסיה\n\n"
        "<b>🏠 משק בית</b>\n/household - 🏠 משק בית\n/familygroup - 👨👩👧👦 קבוצה משפחתית\n/shopping - 🛒 קניות\n/chore - 📌 משימה\n\n"
        "<b>🎓 אקדמיה</b>\n/academy - 🎓 אקדמיה\n/crypto - ₿ מבוא לקריפטו\n/cbdc - 🏦 CBDC\n/decentral - 🌐 ביזור\n/socio - 👥 סוציו-אקונומי\n"
        "/anti - 🛡️ אנטי-שביר\n/edu - 📚 חינוך\n/academy_extended - 📖 אקדמיה מתקדמת\n/academy_nft - 🖼️ NFT\n/academy_dao - 🏛️ DAO\n"
        "/vision - 🔭 חזון\n/spark - ✨ ספארק\n/course_progress - 📈 התקדמות\n/seed_courses - 🌱 זרע קורסים\n\n"
        "<b>👥 קהילה</b>\n/ref - 🔗 הפניה\n/qr - 📱 QR\n/stats - 📊 סטטיסטיקות\n/top - 🏆 מובילים\n/tip - 💸 טיפ\n/contact - 📧 יצירת קשר\n"
        "/faq - ❓ שאלות נפוצות\n/daily - 📅 יומי\n/mydata - 📁 הנתונים שלי\n/gift - 🎁 מתנה\n\n"
        "<b>💖 תרומות</b>\n/donate - 💖 תרומה\n\n"
        "<b>🛠️ כלים</b>\n/help - ❔ עזרה\n/menu - 📋 תפריט\n/language - 🌐 שפה\n/miniapp - 📱 מיני-אפ\n/keyboard - ⌨️ מקלדת\n/hide - 🙈 הסתר\n"
        "/ask - 🤖 שאל\n/feedback - 📝 משוב\n/quiz - ❓ חידון\n/ai - 🧠 AI\n/architecture - 🏗️ ארכיטקטורה\n\n"
        "<b>⭐ אודות</b>\n/whyus - ⭐ למה אנחנו\n/familyguide - 📘 מדריך משפחתי\n\n"
        "<b>🔒 ניהול</b>\n/admin - 🔒 אדמין\n/export - 📤 ייצא\n/debug - 🐛 דיבאג\n/addgroup - ➕ הוסף קבוצה\n/groups - 👥 קבוצות\n"
        "/report - 📊 דוח מערכת\n/setrole - 🎭 קבע תפקיד\n\n"
        "<b>🏙️ TON City</b>\n/city - 🏙️ TON City\n/market - 📈 בורסה\n\n"
        "💡 <i>השתמש בכפתור Menu (☰) כדי לראות את הפקודות בכל רגע.</i>"
    )
    await msg.answer(text, parse_mode='HTML')