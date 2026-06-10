from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.database.session import async_session
from sqlalchemy import text

router = Router()

# שלב 1: בחירת תפקיד
ROLE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎓 סטודנט"), KeyboardButton(text="💼 עצמאי")],
        [KeyboardButton(text="👨👩👧 משפחה"), KeyboardButton(text="🚀 יזם")],
        [KeyboardButton(text="📈 משקיע"), KeyboardButton(text="🌍 אחר")]
    ],
    resize_keyboard=True
)

# שלב 2: בחירת מטרה
GOAL_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 לחסוך כסף"), KeyboardButton(text="📈 ללמוד השקעות")],
        [KeyboardButton(text="🤖 להשתמש ב-AI"), KeyboardButton(text="🎓 ללמוד פיננסים")],
        [KeyboardButton(text="🌍 להצטרף לקהילה")]
    ],
    resize_keyboard=True
)

@router.message(Command("onboarding"))
async def start_onboarding(msg: Message):
    await msg.answer(
        "🌍 ברוכים הבאים ל-Tax Free World!\n\n"
        "בוא נכיר אותך  מה התפקיד שלך?",
        reply_markup=ROLE_KEYBOARD
    )

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
    uid = msg.from_user.id
    async with async_session() as s:
        await s.execute(
            text("INSERT OR REPLACE INTO user_preferences (user_id, role, onboarding_completed) VALUES (:uid, :role, 0)"),
            {"uid": uid, "role": role}
        )
        await s.commit()
    await msg.answer(
        f"✅ תודה! התפקיד שלך הוגדר כ-{msg.text}.\n\n"
        f"מה המטרה העיקרית שלך כרגע?",
        reply_markup=GOAL_KEYBOARD
    )

@router.message(F.text.in_(["💰 לחסוך כסף", "📈 ללמוד השקעות", "🤖 להשתמש ב-AI", "🎓 ללמוד פיננסים", "🌍 להצטרף לקהילה"]))
async def set_goal(msg: Message):
    goal_map = {
        "💰 לחסוך כסף": "save",
        "📈 ללמוד השקעות": "invest",
        "🤖 להשתמש ב-AI": "ai",
        "🎓 ללמוד פיננסים": "learn",
        "🌍 להצטרף לקהילה": "community"
    }
    goal = goal_map[msg.text]
    uid = msg.from_user.id
    async with async_session() as s:
        await s.execute(
            text("UPDATE user_preferences SET goal = :goal, onboarding_completed = 1 WHERE user_id = :uid"),
            {"goal": goal, "uid": uid}
        )
        await s.commit()
    await msg.answer(
        "🎉 מצוין! הכנתי עבורך דשבורד מותאם.\n"
        "שלח /home כדי להתחיל.",
        reply_markup=None
    )
    # הפעל דשבורד
    from bot.routers.dashboard_simple import home
    await home(msg)
