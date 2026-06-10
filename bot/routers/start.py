from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.database.session import async_session
from sqlalchemy import text

router = Router()

def home_keyboard():
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
    uid = msg.from_user.id
    async with async_session() as s:
        prefs = await s.execute(text("SELECT onboarding_completed FROM user_preferences WHERE user_id = :uid"), {"uid": uid})
        row = prefs.fetchone()
        if row and row[0]:
            await home(msg)
            return
    await msg.answer("🌍 ברוכים הבאים ל-Tax Free World!\n\nשלח /home להתחלה", reply_markup=home_keyboard())
    await s.execute(text("INSERT OR IGNORE INTO user_preferences (user_id, onboarding_completed) VALUES (:uid, 1)"), {"uid": uid})
    await s.commit()

@router.message(Command("home"))
@router.message(F.text == "🏠 Home")
async def home(msg: Message):
    await msg.answer("🏠 <b>Tax Free World  מסך ראשי</b>\n\nבחר/י קטגוריה:", parse_mode="HTML", reply_markup=home_keyboard())

@router.message(F.text == "💰 Wealth")
async def wealth(msg: Message):
    kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📊 תקציב"), KeyboardButton(text="📈 פנסיה")],[KeyboardButton(text="➕ הוצאה"), KeyboardButton(text="💰 הכנסה")],[KeyboardButton(text="🔙 חזור")]], resize_keyboard=True)
    await msg.answer("💰 <b>מרכז העושר</b>\n\nבחר/י:", parse_mode="HTML", reply_markup=kb)

@router.message(F.text == "📊 תקציב")
async def budget_btn(msg: Message): await msg.answer("/budget")
@router.message(F.text == "📈 פנסיה")
async def pension_btn(msg: Message): await msg.answer("/pension")
@router.message(F.text == "➕ הוצאה")
async def expense_btn(msg: Message): await msg.answer("/adde")
@router.message(F.text == "💰 הכנסה")
async def income_btn(msg: Message): await msg.answer("/addincome")

@router.message(F.text == "🎓 Learn")
async def learn(msg: Message): await msg.answer("/academy")
@router.message(F.text == "🤖 AI")
async def ai(msg: Message): await msg.answer("/useless")
@router.message(F.text == "🌍 Community")
async def community(msg: Message): await msg.answer("/familygroup")
@router.message(F.text == "🎁 Rewards")
async def rewards(msg: Message): await msg.answer("/top")
@router.message(F.text == "👤 Profile")
async def profile_short(msg: Message): await msg.answer("/profile")
@router.message(F.text == "⚙️ Settings")
async def settings(msg: Message): await msg.answer("/language")
@router.message(F.text == "🔙 חזור")
async def back_home(msg: Message): await home(msg)
