from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.database.session import async_session
from sqlalchemy import text

router = Router()

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏠 Home"), KeyboardButton(text="💰 Wealth")],
            [KeyboardButton(text="🎓 Learn"), KeyboardButton(text="🤖 AI")],
            [KeyboardButton(text="🌍 Community"), KeyboardButton(text="🎁 Rewards")],
            [KeyboardButton(text="👤 Profile"), KeyboardButton(text="⚙️ Settings")]
        ],
        resize_keyboard=True
    )

@router.message(Command('start'))
async def cmd_start(msg: Message):
    from bot.routers.welcome_onboarding import cmd_start as onboarding_start
    await onboarding_start(msg)
