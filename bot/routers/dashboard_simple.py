from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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

@router.message(Command("home"))
@router.message(F.text == "🏠 Home")
async def home(msg: Message):
    await msg.answer("🏠 Tax Free World  Dashboard", reply_markup=get_main_keyboard())

# ---- Wealth תת‑תפריט ----
@router.message(F.text == "💰 Wealth")
async def wealth(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 תקציב", callback_data="cmd_budget"),
         InlineKeyboardButton(text="➕ הוצאה", callback_data="cmd_adde")],
        [InlineKeyboardButton(text="📈 פנסיה", callback_data="cmd_pension")]
    ])
    await msg.answer("💰 מרכז העושר  בחר פעולה:", reply_markup=kb)

@router.callback_query(F.data == "cmd_budget")
async def go_budget(callback): 
    await callback.message.answer("/budget")
    await callback.answer()

@router.callback_query(F.data == "cmd_adde")
async def go_adde(callback):
    await callback.message.answer("/adde 0")
    await callback.answer()

@router.callback_query(F.data == "cmd_pension")
async def go_pension(callback):
    await callback.message.answer("/pension")
    await callback.answer()

# ---- Learn תת‑תפריט ----
@router.message(F.text == "🎓 Learn")
async def learn(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 אקדמיה", callback_data="cmd_academy"),
         InlineKeyboardButton(text="🤖 AI", callback_data="cmd_useless")]
    ])
    await msg.answer("🎓 למידה  בחר:", reply_markup=kb)

@router.callback_query(F.data == "cmd_academy")
async def go_academy(callback):
    await callback.message.answer("/academy")
    await callback.answer()

@router.callback_query(F.data == "cmd_useless")
async def go_useless(callback):
    await callback.message.answer("/useless")
    await callback.answer()

# ---- Community / Rewards / Profile / Settings ----
@router.message(F.text == "🌍 Community")
async def community(msg): await msg.answer("/familygroup")
@router.message(F.text == "🎁 Rewards")
async def rewards(msg): await msg.answer("/top")
@router.message(F.text == "👤 Profile")
async def profile_short(msg): await msg.answer("/profile")
@router.message(F.text == "⚙️ Settings")
async def settings(msg): await msg.answer("/language")
