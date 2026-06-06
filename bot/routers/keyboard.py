from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from bot.keyboards.inline import savings_menu, household_menu, academy_menu, community_menu
from bot.messages.he import MESSAGES
from bot.routers.daily import daily_handler

router = Router()

# מקלדת משותפת
reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 חיסכון"), KeyboardButton(text="🏠 כלכלת הבית")],
        [KeyboardButton(text="📚 אקדמיה"), KeyboardButton(text="👥 קהילה")],
        [KeyboardButton(text="📱 מחשבון ויזואלי"), KeyboardButton(text="📈 סיכום יומי")],
    ],
    resize_keyboard=True
)

@router.message(Command("keyboard"))
async def show_keyboard(msg: Message):
    await msg.answer("בחר פעולה:", reply_markup=reply_kb)

@router.message(F.text == "💰 חיסכון")
async def btn_savings(msg: Message):
    await msg.answer("💰 <b>חיסכון ועמלות</b>", parse_mode="HTML", reply_markup=savings_menu())

@router.message(F.text == "🏠 כלכלת הבית")
async def btn_household(msg: Message):
    await msg.answer("🏠 <b>ניהול כלכלת הבית</b>", parse_mode="HTML", reply_markup=household_menu())

@router.message(F.text == "📚 אקדמיה")
async def btn_academy(msg: Message):
    await msg.answer("📚 <b>אקדמיה</b>", parse_mode="HTML", reply_markup=academy_menu())

@router.message(F.text == "👥 קהילה")
async def btn_community(msg: Message):
    await msg.answer("👥 <b>קהילה וכלים</b>", parse_mode="HTML", reply_markup=community_menu())

@router.message(F.text == "📈 סיכום יומי")
async def btn_daily(msg: Message):
    await daily_handler(msg)

@router.message(Command("hide"))
async def hide_keyboard(msg: Message):
    await msg.answer("המקלדת הוסתרה.", reply_markup=ReplyKeyboardRemove())
