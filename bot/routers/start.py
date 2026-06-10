from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select, text

router = Router()

@router.message(Command('start'))
async def cmd_start(msg: Message):
    uid = msg.from_user.id
    async with async_session() as s:
        # בדוק אם המשתמש כבר השלים onboarding
        prefs = await s.execute(text("SELECT onboarding_completed FROM user_preferences WHERE user_id = :uid"), {"uid": uid})
        row = prefs.fetchone()
        if row and row[0]:
            from bot.routers.dashboard import show_dashboard
from bot.routers.expenses import router as expenses_router
            await show_dashboard(msg)
            return
    await msg.answer("🌍 ברוכים הבאים ל-Tax Free World!\n\nנתחיל בלהכיר אותך...")
    from bot.routers.welcome import start_onboarding
    await start_onboarding(msg)

