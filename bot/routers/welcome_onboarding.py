from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from sqlalchemy import text
from bot.utils.i18n import i18n

router = Router()

def get_role_keyboard(lang="en"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎓 Student / Beginner" if lang=="en" else "🎓 סטודנט / מתחיל", callback_data="role_student")],
        [InlineKeyboardButton(text="💼 Entrepreneur" if lang=="en" else "💼 עצמאי / יזם", callback_data="role_business")],
        [InlineKeyboardButton(text="👨👩👧 Family" if lang=="en" else "👨👩👧 משפחה", callback_data="role_family")],
        [InlineKeyboardButton(text="📈 Investor" if lang=="en" else "📈 משקיע", callback_data="role_investor")]
    ])

@router.message(Command("start"))
async def cmd_start(msg: Message):
    uid = msg.from_user.id
    lang = "he"  # ניתן לשפר בהמשך לפי user_preferences
    
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
