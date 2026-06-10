from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from sqlalchemy import text
from bot.utils.i18n import i18n

router = Router()

def get_role_keyboard(lang="he"):
    if lang == "en":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎓 Student / Beginner", callback_data="role_student")],
            [InlineKeyboardButton(text="💼 Entrepreneur", callback_data="role_business")],
            [InlineKeyboardButton(text="👨👩👧 Family", callback_data="role_family")],
            [InlineKeyboardButton(text="📈 Investor", callback_data="role_investor")]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎓 סטודנט / מתחיל", callback_data="role_student")],
            [InlineKeyboardButton(text="💼 עצמאי / יזם", callback_data="role_business")],
            [InlineKeyboardButton(text="👨👩👧 משפחה", callback_data="role_family")],
            [InlineKeyboardButton(text="📈 משקיע", callback_data="role_investor")]
        ])

@router.message(Command("start"))
async def cmd_start(msg: Message):
    uid = msg.from_user.id
    lang = "he"

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

    await msg.answer(
        i18n.get("welcome", lang),
        parse_mode="HTML",
        reply_markup=get_role_keyboard(lang)
    )

@router.callback_query(F.data.startswith("role_"))
async def process_role(callback: CallbackQuery):
    role = callback.data.split("_")[1]
    uid = callback.from_user.id
    
    async with async_session() as s:
        await s.execute(
            text("INSERT OR REPLACE INTO user_preferences (user_id, role, onboarding_completed) VALUES (:uid, :role, 0)"),
            {"uid": uid, "role": role}
        )
        await s.commit()
    
    await callback.message.edit_text("✅ תודה! עכשיו בחר את המטרה העיקרית שלך:")
    await callback.answer()
