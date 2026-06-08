from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import PensionProfile
from sqlalchemy import select
from bot.services.pension_calc import calc_accumulating, calc_budgetary, estimate_tax

router = Router()
user_data = {}

@router.message(Command("pension"))
async def cmd_pension(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏛 עובד מדינה / ציבורי", callback_data="employee_public")],
        [InlineKeyboardButton(text="🏢 עובד פרטי / עצמאי", callback_data="employee_private")],
        [InlineKeyboardButton(text="❓ לא בטוח", callback_data="employee_unknown")]
    ])
    await msg.answer(
        "📊 <b>מחשבון פנסיה  TON Israel</b>\n\n"
        "איפה אתה עובד?",
        parse_mode="HTML", reply_markup=kb
    )

@router.callback_query(F.data.startswith("employee_"))
async def employee_chosen(callback: CallbackQuery):
    emp_type = callback.data.split("_")[1]
    uid = callback.from_user.id
    user_data[uid] = {"employee_type": emp_type, "step": "age"}
    async with async_session() as session:
        profile = PensionProfile(telegram_id=uid, employee_type=emp_type)
        session.add(profile)
        await session.commit()
    await callback.message.answer("מה גילך?")
    await callback.answer()

@router.message(F.text.regexp(r'^\d+$'))
async def handle_number(msg: Message):
    uid = msg.from_user.id
    if uid not in user_data:
        return
    step = user_data[uid].get("step")
    val = int(msg.text)
    if step == "age":
        user_data[uid]["age_now"] = val
        user_data[uid]["step"] = "retirement_age"
        await msg.answer("גיל פרישה?")
    elif step == "retirement_age":
        user_data[uid]["retirement_age"] = val
        user_data[uid]["step"] = "salary"
        await msg.answer("שכר ברוטו חודשי?")
    elif step == "salary":
        user_data[uid]["salary_bruto"] = float(val)
        user_data[uid]["step"] = "seniority"
        await msg.answer("ותק בעבודה (שנים)?")
    elif step == "seniority":
        user_data[uid]["seniority_years"] = val
        # אם עובד פרטי  אוסף נתונים צוברים; אחרת מחשב תקציבית
        if user_data[uid]["employee_type"] == "public":
            # חישוב תקציבי ישיר
            profile = user_data.pop(uid)
            result = calc_budgetary(profile)
            tax = estimate_tax(result["monthly_pension"])
            await msg.answer(
                f"💰 <b>פנסיה תקציבית</b>\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"📆 קצבה חודשית: {result['monthly_pension']:,.0f} שח\n"
                f"⚖ מס מוערך: {tax:,.0f} שח\n"
                f"📥 נטו: {result['monthly_pension']-tax:,.0f} שח",
                parse_mode="HTML"
            )
        else:
            user_data[uid]["step"] = "contribution_employee"
            await msg.answer("אחוז הפרשה שלך? (לדוגמה: 6)")
    elif step == "contribution_employee":
        user_data[uid]["contribution_employee"] = float(val)
        user_data[uid]["step"] = "contribution_employer"
        await msg.answer("אחוז הפרשת מעסיק? (לדוגמה: 6.5)")
    elif step == "contribution_employer":
        user_data[uid]["contribution_employer"] = float(val)
        user_data[uid]["step"] = "expected_return"
        await msg.answer("תשואה שנתית משוערת? (לדוגמה: 5.2)")
    elif step == "expected_return":
        user_data[uid]["expected_return"] = float(val)
        user_data[uid]["step"] = "management_fees"
        await msg.answer("דמי ניהול שנתיים? (לדוגמה: 0.5)")
    elif step == "management_fees":
        user_data[uid]["management_fees"] = float(val)
        # חישוב צובר
        profile = user_data.pop(uid)
        profile["current_capital"] = 0  # לא נאסף כרגע
        result = calc_accumulating(profile)
        tax = estimate_tax(result["monthly_pension"])
        # שמירה ב‑DB
        async with async_session() as session:
            p = await session.get(PensionProfile, (await session.execute(select(PensionProfile).where(PensionProfile.telegram_id == uid))).scalar_one_or_none().id if ... else None)
            # עדכון פשוט יותר: ניצור רשומה חדשה או נעדכן
            # (לפשט: create new for now)
            p = PensionProfile(
                telegram_id=uid,
                employee_type=profile["employee_type"],
                pension_type="accumulating",
                age_now=profile["age_now"],
                retirement_age=profile["retirement_age"],
                salary_bruto=profile["salary_bruto"],
                seniority_years=profile.get("seniority_years", 0),
                contribution_employee=profile["contribution_employee"],
                contribution_employer=profile["contribution_employer"],
                expected_return=profile["expected_return"],
                management_fees=profile["management_fees"],
                result_capital=result["capital"],
                result_monthly=result["monthly_pension"]
            )
            session.add(p)
            await session.commit()
        await msg.answer(
            f"📊 <b>תוצאת חישוב</b>\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"💰 צבירה: {result['capital']:,.0f} שח\n"
            f"📆 קצבה: {result['monthly_pension']:,.0f} שח\n"
            f"⚖ מס: {tax:,.0f} שח\n"
            f"📥 נטו: {result['monthly_pension']-tax:,.0f} שח",
            parse_mode="HTML"
        )
