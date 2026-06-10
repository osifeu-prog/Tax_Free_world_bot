from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import text
from bot.database.session import engine
import logging

router = Router()
logger = logging.getLogger(__name__)

ROLE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎓 סטודנט"), KeyboardButton(text="💼 עצמאי")],
        [KeyboardButton(text="👨👩👧 משפחה"), KeyboardButton(text="🚀 יזם")],
        [KeyboardButton(text="📈 משקיע"), KeyboardButton(text="🌍 אחר")]
    ],
    resize_keyboard=True
)

async def save_user_role(user_id: int, role: str):
    async with engine.begin() as conn:
        await conn.execute(
            text("INSERT OR REPLACE INTO user_preferences (user_id, role, onboarding_completed) VALUES (:uid, :role, 1)"),
            {"uid": user_id, "role": role}
        )

async def get_user_role(user_id: int):
    async with engine.begin() as conn:
        res = await conn.execute(
            text("SELECT role FROM user_preferences WHERE user_id = :uid"),
            {"uid": user_id}
        )
        row = res.fetchone()
        return row[0] if row else "citizen"

@router.message(Command("onboarding"))
async def start_onboarding(msg: Message):
    await msg.answer("🌍 ברוכים הבאים ל-Tax Free World!\n\nמי אתה? (בחר/י)", reply_markup=ROLE_KEYBOARD)

@router.message(F.text.in_(["🎓 סטודנט", "💼 עצמאי", "👨👩👧 משפחה", "🚀 יזם", "📈 משקיע", "🌍 אחר"]))
async def set_role(msg: Message):
    role_map = {
        "🎓 סטודנט": "student",
        "💼 עצמאי": "entrepreneur",
        "👨👩👧 משפחה": "family",
        "🚀 יזם": "founder",
        "📈 משקיע": "investor",
        "🌍 אחר": "citizen"
    }
    role = role_map[msg.text]
    await save_user_role(msg.from_user.id, role)
    await msg.answer(f"✅ תודה! התפקיד שלך הוגדר כ-{msg.text}.\n\nנוכל כעת להתאים לך את החוויה.", reply_markup=None)
    from bot.routers.dashboard import show_dashboard
    await show_dashboard(msg)
