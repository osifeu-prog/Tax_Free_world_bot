from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from sqlalchemy import text

router = Router()

def get_role_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎓 Student / Beginner", callback_data="role_student")],
        [InlineKeyboardButton(text="💼 Self-employed / Entrepreneur", callback_data="role_business")],
        [InlineKeyboardButton(text="👨👩👧 Family", callback_data="role_family")],
        [InlineKeyboardButton(text="📈 Investor", callback_data="role_investor")],
        [InlineKeyboardButton(text="🌍 Other", callback_data="role_other")]
    ])

def get_goals_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Save more money", callback_data="goal_save")],
        [InlineKeyboardButton(text="📚 Learn finance", callback_data="goal_learn")],
        [InlineKeyboardButton(text="🚀 Invest better", callback_data="goal_invest")],
        [InlineKeyboardButton(text="🤝 Join community", callback_data="goal_community")],
        [InlineKeyboardButton(text="🎯 All of the above", callback_data="goal_all")]
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

    await msg.answer(
        "🌍 <b>Welcome to Tax Free World 2.0!</b>\n\n"
        "We're here to help you learn, save, invest, and build a better financial future.\n\n"
        "To personalize your experience, please choose your role:",
        parse_mode="HTML",
        reply_markup=get_role_keyboard()
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
    
    await callback.message.edit_text(
        "✅ Thank you! Now tell us your main goal:",
        reply_markup=get_goals_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data.startswith("goal_"))
async def process_goal(callback: CallbackQuery):
    goal = callback.data.split("_")[1]
    uid = callback.from_user.id
    
    async with async_session() as s:
        await s.execute(
            text("UPDATE user_preferences SET goal = :goal, onboarding_completed = 1 WHERE user_id = :uid"),
            {"goal": goal, "uid": uid}
        )
        await s.commit()
    
    await callback.message.edit_text(
        "🎉 <b>Onboarding completed!</b>\n\n"
        "Welcome to your journey toward financial freedom.\n\n"
        "Send /home to enter your personal dashboard.",
        parse_mode="HTML"
    )
    await callback.answer()
