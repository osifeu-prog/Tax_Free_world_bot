from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

def start_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 מחשבון עמלות", callback_data="compare_prompt")],
        [InlineKeyboardButton(text="👛 איך פותחים ארנק", callback_data="wallet")],
        [InlineKeyboardButton(text="🔍 למה TON?", callback_data="why")],
        [InlineKeyboardButton(text="🏢 לעסקים", callback_data="business")],
        [InlineKeyboardButton(text="📱 מחשבון ויזואלי", web_app=WebAppInfo(url="https://your-domain.com/landing/miniapp.html"))],
        [InlineKeyboardButton(text="🔗 הקוד שלי להפצה", callback_data="my_ref")],
        [InlineKeyboardButton(text="📬 צור קשר", callback_data="contact")],
        [InlineKeyboardButton(text="ℹ️ עזרה", callback_data="help")],
    ])

def back_to_start():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 חזרה לתפריט", callback_data="start")]
    ])
