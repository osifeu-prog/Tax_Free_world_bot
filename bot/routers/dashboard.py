from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.database.session import engine
from sqlalchemy import text

router = Router()

def main_dashboard_keyboard():
    buttons = [
        [KeyboardButton(text="🏠 Home"), KeyboardButton(text="💰 Wealth")],
        [KeyboardButton(text="🎓 Learn"), KeyboardButton(text="🤖 AI")],
        [KeyboardButton(text="🌍 Community"), KeyboardButton(text="🎁 Rewards")],
        [KeyboardButton(text="👤 Profile"), KeyboardButton(text="⚙️ Settings")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

async def show_dashboard(msg: Message):
    await msg.answer("🏠 <b>Tax Free World  דשבורד ראשי</b>\n\nבחר/י קטגוריה:", parse_mode="HTML", reply_markup=main_dashboard_keyboard())

@router.message(Command("home"))
@router.message(F.text == "🏠 Home")
async def cmd_home(msg: Message):
    await show_dashboard(msg)

@router.message(F.text == "💰 Wealth")
async def cmd_wealth(msg: Message):
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📊 חיסכון"), KeyboardButton(text="📈 פנסיה")],[KeyboardButton(text="💰 תקציב"), KeyboardButton(text="🔙 חזור")]], resize_keyboard=True)
    await msg.answer("💰 <b>מרכז העושר</b>\n\nבחר/י נושא:", parse_mode="HTML", reply_markup=kb)

@router.message(F.text == "🎓 Learn")
async def cmd_learn(msg: Message):
    await msg.answer("/academy")

@router.message(F.text == "🤖 AI")
async def cmd_ai(msg: Message):
    await msg.answer("/useless")

@router.message(F.text == "🌍 Community")
async def cmd_community(msg: Message):
    await msg.answer("/familygroup")

@router.message(F.text == "🎁 Rewards")
async def cmd_rewards(msg: Message):
    await msg.answer("/top")

@router.message(F.text == "👤 Profile")
async def cmd_profile_short(msg: Message):
    await msg.answer("/profile")

@router.message(F.text == "⚙️ Settings")
async def cmd_settings(msg: Message):
    await msg.answer("/language")

@router.message(F.text == "🔙 חזור")

@router.callback_query(F.data == "quick_adde")
async def quick_adde(callback):
    await callback.message.answer("לדוגמה: /adde 50 אוכל")
    await callback.answer()

@router.callback_query(F.data == "quick_expenses")
async def quick_expenses(callback):
    await callback.message.answer("/expenses")
    await callback.answer()

(msg: Message):
    await show_dashboard(msg)

