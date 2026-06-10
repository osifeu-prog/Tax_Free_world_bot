from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from bot.database.session import async_session
from sqlalchemy import text

router = Router()

def get_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ הוצאה"), KeyboardButton(text="💰 הכנסה")],
            [KeyboardButton(text="📊 פנסיה"), KeyboardButton(text="💖 תרומה")],
            [KeyboardButton(text="🎓 אקדמיה"), KeyboardButton(text="🤖 AI")],
            [KeyboardButton(text="🏠 Dashboard"), KeyboardButton(text="📋 עזרה")]
        ],
        resize_keyboard=True
    )

@router.message(Command('start'))
async def cmd_start(msg: Message):
    uid = msg.from_user.id
    async with async_session() as s:
        # בדוק onboarding
        prefs = await s.execute(text("SELECT onboarding_completed FROM user_preferences WHERE user_id = :uid"), {"uid": uid})
        row = prefs.fetchone()
        if row and row[0]:
            # from bot.routers.dashboard import show_dashboard (disabled)
            await msg.answer('🏠 Dashboard זמני  /menu לפעולות')
            return
    await msg.answer("🌍 ברוכים הבאים ל-Tax Free World!\n\nנתחיל בלהכיר אותך...")
    from bot.routers.welcome import start_onboarding
    await start_onboarding(msg)

@router.callback_query(F.data.startswith('quick_'))
async def quick_actions(callback: CallbackQuery):
    if callback.data == "quick_adde":
        await callback.message.answer("לדוגמה: /adde 50 אוכל")
    elif callback.data == "quick_expenses":
        await callback.message.answer("/expenses")
    await callback.answer()

