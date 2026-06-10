from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.database.session import async_session
from sqlalchemy import text
from bot.routers.dashboard_simple import home
from bot.routers.welcome_onboarding import start_onboarding

router = Router()

@router.message(Command('start'))
async def cmd_start(msg: Message):
    uid = msg.from_user.id
    async with async_session() as s:
        prefs = await s.execute(text("SELECT onboarding_completed FROM user_preferences WHERE user_id = :uid"), {"uid": uid})
        row = prefs.fetchone()
        if row and row[0] == 1:
            await home(msg)
            return
    await msg.answer("👋 ברוכים הבאים ל-Tax Free World!\n\nנתחיל בתהליך הכרות קצר...")
    await start_onboarding(msg)

