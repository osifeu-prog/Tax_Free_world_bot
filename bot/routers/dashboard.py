from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

def dashboard_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏠 Home")],
            [KeyboardButton(text="💰 Wealth"), KeyboardButton(text="🎓 Learn")],
            [KeyboardButton(text="🤖 AI"), KeyboardButton(text="🌍 Community")],
            [KeyboardButton(text="👤 Profile"), KeyboardButton(text="⚙️ Settings")]
        ],
        resize_keyboard=True
    )

@router.message(Command("dashboard"))
async def cmd_dashboard(msg: Message):
    await msg.answer("🏠 <b>Tax Free World Dashboard</b>", parse_mode="HTML", reply_markup=dashboard_keyboard())

@router.message(F.text == "🏠 Home")
async def home_action(msg: Message):
    await cmd_dashboard(msg)

@router.message(F.text == "💰 Wealth")
async def wealth_action(msg: Message):
    await msg.answer("/budget")

@router.message(F.text == "🎓 Learn")
async def learn_action(msg: Message):
    await msg.answer("/academy")

@router.message(F.text == "🤖 AI")
async def ai_action(msg: Message):
    await msg.answer("/useless")

@router.message(F.text == "🌍 Community")
async def community_action(msg: Message):
    await msg.answer("/familygroup")

@router.message(F.text == "👤 Profile")
async def profile_action(msg: Message):
    await msg.answer("/profile")

@router.message(F.text == "⚙️ Settings")
async def settings_action(msg: Message):
    await msg.answer("/language")
