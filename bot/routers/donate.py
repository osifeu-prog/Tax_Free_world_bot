from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("donate"))
async def cmd_donate(msg: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❤️ 50 TON", callback_data="donate_50")],
        [InlineKeyboardButton(text="💛 100 TON", callback_data="donate_100")],
        [InlineKeyboardButton(text="💚 500 TON", callback_data="donate_500")],
        [InlineKeyboardButton(text="💙 סכום מותאם אישית", callback_data="donate_custom")]
    ])
    await msg.answer(
        "💖 <b>תרומה לפרויקט TON Israel</b>\n\n"
        "הפרויקט חופשי ומתוחזק על ידי קהילה.\n"
        "כל תרומה עוזרת לנו להמשיך לפתח ולשפר.\n\n"
        "בחר סכום או סכום מותאם אישית:",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("donate_"))
async def process_donate(callback: CallbackQuery):
    amount = callback.data.split("_")[1]
    if amount == "custom":
        await callback.message.answer("📝 אנא שלח את הסכום (במספרים):")
    else:
        await callback.message.answer(f"✅ תודה על תרומת {amount} TON! 🙏")
    await callback.answer()
