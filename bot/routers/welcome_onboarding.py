from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from sqlalchemy import text
from bot.utils.i18n import i18n

router = Router()

def get_role_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎓 סטודנט / מתחיל", callback_data="role_student")],
        [InlineKeyboardButton(text="💼 עצמאי / יזם", callback_data="role_business")],
        [InlineKeyboardButton(text="👨👩👧 משפחה", callback_data="role_family")],
        [InlineKeyboardButton(text="📈 משקיע", callback_data="role_investor")]
    ])

@router.message(Command("start"))
async def cmd_start(msg: Message):
    uid = msg.from_user.id
    
    async with async_session() as s:
        result = await s.execute(
            text("SELECT onboarding_completed FROM user_preferences WHERE user_id = :uid"),
            {"uid": uid}
        )
        row = result.fetchone()
        
        if row and row[0]:
            from bot.routers.dashboard_simple import home
            await home(msg)
            return

    # Onboarding חדש
    await msg.answer(
        "🌍 <b>ברוכים הבאים ל-Tax Free World 2.0!</b>\n\n"
        "כדי להתאים לך את החוויה, בחר את התפקיד שלך:",
        parse_mode="HTML",
        reply_markup=get_role_keyboard()
    )

@router.callback_query(F.data.startswith("role_"))
async def process_role(callback: CallbackQuery):
    role = callback.data.split("_")[1]
    uid = callback.from_user.id
    
    async with async_session() as s:
        await s.execute(
            text("INSERT OR REPLACE INTO user_preferences (user_id, role, onboarding_completed) VALUES (:uid, :role, 1)"),
            {"uid": uid, "role": role}
        )
        await s.commit()
    
    await callback.message.edit_text(
        "✅ תודה! ההרשמה הושלמה.\n\nשלח /home כדי להיכנס לדשבורד האישי.",
        parse_mode="HTML"
    )
    await callback.answer()

