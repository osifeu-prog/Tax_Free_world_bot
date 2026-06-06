from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

def start_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 מחשבון עמלות", callback_data="compare_prompt")],
        [InlineKeyboardButton(text="📊 תרחישים מהירים", callback_data="presets")],
        [InlineKeyboardButton(text="🏠 מחשבון תקציב", callback_data="budget_prompt")],
        [InlineKeyboardButton(text="👛 איך פותחים ארנק", callback_data="wallet")],
        [InlineKeyboardButton(text="📱 מחשבון ויזואלי", web_app=WebAppInfo(url="https://taxfreeworldbot-production.up.railway.app/landing/miniapp.html"))],
        [InlineKeyboardButton(text="📚 אקדמיה  ללמוד", callback_data="academy")],
        [InlineKeyboardButton(text="🔗 הקוד שלי להפצה", callback_data="my_ref")],
        [InlineKeyboardButton(text="💡 טיפ יומי", callback_data="tip")],
        [InlineKeyboardButton(text="🏆 לוח מובילים", callback_data="top")],
        [InlineKeyboardButton(text="📊 סטטיסטיקות", callback_data="stats")],
        [InlineKeyboardButton(text="📬 צור קשר", callback_data="contact")],
        [InlineKeyboardButton(text="ℹ️ עזרה", callback_data="help")],
    ])

def back_to_start():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 חזרה לתפריט", callback_data="start")]
    ])

def academy_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪙 מה זה קריפטו?", callback_data="crypto")],
        [InlineKeyboardButton(text="🏦 מה זה CBDC?", callback_data="cbdc")],
        [InlineKeyboardButton(text="🔓 ביזור מול ריכוזיות", callback_data="decentral")],
        [InlineKeyboardButton(text="🌿 סוציוקרטיה", callback_data="socio")],
        [InlineKeyboardButton(text="🛡️ טכנולוגיות נגד שחיתות", callback_data="anti")],
        [InlineKeyboardButton(text="🎓 חינוך, כלכלה ורווחה", callback_data="edu")],
        [InlineKeyboardButton(text="❓ שאלות נפוצות", callback_data="faq")],
        [InlineKeyboardButton(text="🔙 חזרה", callback_data="start")],
    ])

def presets_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏠 שכר דירה (2,500)", callback_data="preset_2500_1")],
        [InlineKeyboardButton(text="💰 משכורת (10,000)", callback_data="preset_10000_2")],
        [InlineKeyboardButton(text="🛒 קניות חודשיות (3,000)", callback_data="preset_3000_4")],
        [InlineKeyboardButton(text="🧑💼 פרילנסר (5,000)", callback_data="preset_5000_3")],
        [InlineKeyboardButton(text="🔙 חזרה", callback_data="start")],
    ])

def share_result(amount, tx):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 שתף את התוצאה", switch_inline_query=f"חסכתי {amount} בעמלות עם TON!")]
    ])
