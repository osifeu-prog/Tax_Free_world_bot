from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import PensionProfile
from sqlalchemy import select

router = Router()

# ===== אשף איסוף נתונים =====
user_data = {}  # זמני  בפרודקשן נעדיף FSM

@router.message(Command("pension"))
async def cmd_pension(msg: Message):
    await msg.answer(
        "📊 <b>מחשבון פנסיה</b>\n\n"
        "נחשב יחד את הפנסיה הצפויה שלך.\n"
        "נתחיל  מה גילך? (מספר)",
        parse_mode="HTML"
    )
    user_data[msg.from_user.id] = {"step": "age"}

@router.message(F.text.regexp(r"^\d+$"))
async def handle_number(msg: Message):
    uid = msg.from_user.id
    if uid not in user_data:
        return  # לא באשף
    step = user_data[uid].get("step")
    val = int(msg.text)

    if step == "age":
        user_data[uid]["age_now"] = val
        user_data[uid]["step"] = "retirement_age"
        await msg.answer("מה גיל הפרישה המתוכנן? (מספר)")
    elif step == "retirement_age":
        user_data[uid]["retirement_age"] = val
        user_data[uid]["step"] = "salary"
        await msg.answer("מה השכר ברוטו החודשי? (ללא פסיקים)")
    elif step == "salary":
        user_data[uid]["salary_bruto"] = float(msg.text)
        user_data[uid]["step"] = "contribution_employee"
        await msg.answer("מה אחוז ההפרשה שלך לפנסיה? (לדוגמה: 6)")
    elif step == "contribution_employee":
        user_data[uid]["contribution_employee"] = float(msg.text)
        user_data[uid]["step"] = "contribution_employer"
        await msg.answer("מה אחוז ההפרשה של המעסיק? (לדוגמה: 6.5)")
    elif step == "contribution_employer":
        user_data[uid]["contribution_employer"] = float(msg.text)
        user_data[uid]["step"] = "expected_return"
        await msg.answer("מה התשואה השנתית המשוערת? (לדוגמה: 5.2)")
    elif step == "expected_return":
        user_data[uid]["expected_return"] = float(msg.text)
        user_data[uid]["step"] = "management_fees"
        await msg.answer("מה דמי הניהול השנתיים? (לדוגמה: 0.5)")
    elif step == "management_fees":
        user_data[uid]["management_fees"] = float(msg.text)
        # ===== סיום איסוף  חישוב =====
        await finalize_pension(msg, user_data.pop(uid))

async def finalize_pension(msg: Message, data: dict):
    # חישוב בסיסי (פנסיה צוברת)
    months_left = (data["retirement_age"] - data["age_now"]) * 12
    monthly_salary = data["salary_bruto"]
    total_contrib = monthly_salary * (data["contribution_employee"] + data["contribution_employer"]) / 100
    # הצטברות עם ריבית דריבית חודשית
    r = (data["expected_return"] / 100) / 12   # monthly rate
    future_value = 0
    for m in range(1, int(months_left) + 1):
        future_value = (future_value + total_contrib) * (1 + r)
    # הפחתת דמי ניהול שנתיים (פשוט)
    future_value *= (1 - data["management_fees"] / 100 * (months_left / 12))
    # חישוב קצבה חודשית (משיכה ל25 שנה)
    months_pension = 25 * 12
    rr = ((1 + r)**months_pension - 1) / (r * (1 + r)**months_pension)
    monthly_pension = future_value / rr

    # שמירה ב‑DB
    async with async_session() as session:
        stmt = select(PensionProfile).where(PensionProfile.telegram_id == msg.from_user.id)
        profile = (await session.execute(stmt)).scalar_one_or_none()
        if not profile:
            profile = PensionProfile(telegram_id=msg.from_user.id)
            session.add(profile)
        for k, v in data.items():
            setattr(profile, k, v)
        profile.result_capital = round(future_value, 2)
        profile.result_monthly = round(monthly_pension, 2)
        await session.commit()

    await msg.answer(
        f"📊 <b>תוצאות החישוב</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"💰 צבירה צפויה בגיל {data['retirement_age']}: <b>{future_value:,.0f} שח</b>\n"
        f"📆 קצבה חודשית משוערת: <b>{monthly_pension:,.0f} שח</b>\n\n"
        f"📌 <i>הערכה בלבד  אינה ייעוץ פנסיוני</i>",
        parse_mode="HTML"
    )
