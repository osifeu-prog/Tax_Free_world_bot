from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from sqlalchemy import text
from bot.utils.i18n import i18n

router = Router()

def get_role_keyboard(lang="en"):
    texts = {
        "en": ["🎓 Student / Beginner", "💼 Entrepreneur", "👨👩👧 Family", "📈 Investor"],
        "he": ["🎓 סטודנט / מתחיל", "💼 עצמאי / יזם", "👨👩👧 משפחה", "📈 משקיע"]
    }
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts[lang][0], callback_data="role_student")],
        [InlineKeyboardButton(text=texts[lang][1], callback_data="role_business")],
        [InlineKeyboardButton(text=texts[lang][2], callback_data="role_family")],
        [InlineKeyboardButton(text=texts[lang][3], callback_data="role_investor")]
    ])

@router.message(Command("start"))
async def cmd_start(msg: Message):
    uid = msg.from_user.id
    lang = "he"  # ברירת מחדל
    
    async with async_session() as s:
        result = await s.execute(
            text("SELECT onboarding_completed, language FROM user_preferences WHERE user_id = :uid"),
            {"uid": uid}
        )
        row = result.fetchone()
        
        if row and row[0]:
            from bot.routers.dashboard_simple import home
            await home(msg)
            return

    await msg.answer(
        i18n.get("welcome", lang),
        parse_mode="HTML",
        reply_markup=get_role_keyboard(lang)
    )

@router.callback_query(F.data.startswith("role_"))
async def process_role(callback: CallbackQuery):
    # ... (המשך הקוד כמו קודם)
    await callback.message.edit_text("✅ Thank you! Now choose your goal:", reply_markup=get_goals_keyboard())
    await callback.answer()

# (הוסף כאן את שאר הפונקציות process_goal כמו בגרסאות קודמות)
