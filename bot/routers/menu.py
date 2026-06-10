from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# תפריט ראשי – מקלדת קבועה (Reply)
def main_keyboard():
    buttons = [
        [KeyboardButton(text='➕ הוצאה'), KeyboardButton(text='💰 הכנסה')],
        [KeyboardButton(text="📊 פרופיל"), KeyboardButton(text="💰 הוצאות")],
        [KeyboardButton(text="📈 פנסיה"), KeyboardButton(text="💖 תרומה")],
        [KeyboardButton(text="🎓 אקדמיה"), KeyboardButton(text="📋 עזרה")],
        [KeyboardButton(text="🤖 יוסלס AI"), KeyboardButton(text="⭐ מובילים")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@router.message(Command("menu"))
async def show_menu(msg: Message):
    await msg.answer("📋 <b>תפריט ראשי – בחר אפשרות</b>", parse_mode="HTML", reply_markup=main_keyboard())

# טיפול בלחיצות על הכפתורים
@router.message(F.text == "📊 פרופיל")
async def menu_profile(msg: Message):
    await msg.answer("/profile")

@router.message(F.text == "💰 הוצאות")
async def menu_expenses(msg: Message):
    await msg.answer("/addexpense")

@router.message(F.text == "📈 פנסיה")
async def menu_pension(msg: Message):
    await msg.answer("/pension")

@router.message(F.text == "💖 תרומה")
async def menu_donate(msg: Message):
    await msg.answer("/donate")

@router.message(F.text == "🎓 אקדמיה")
async def menu_academy(msg: Message):
    await msg.answer("/academy")

@router.message(F.text == "📋 עזרה")
async def menu_help(msg: Message):
    await msg.answer("/help")

@router.message(F.text == "🤖 יוסלס AI")
async def menu_useless(msg: Message):
    await msg.answer("/useless")

@router.message(F.text == "⭐ מובילים")
async def menu_top(msg: Message):
    await msg.answer("/top")

