from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import PensionProfile, User
from sqlalchemy import select
from bot.services.pension_calc import calc_accumulating, calc_budgetary, estimate_tax
from bot.services.translation_service import translator

router = Router()
user_data = {}

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else "he"

@router.message(Command("pension"))
async def cmd_pension(msg: Message):
    lang = await get_lang(msg.from_user.id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏛 " + translator.t(lang, "employee_public"), callback_data="employee_public")],
        [InlineKeyboardButton(text="🏢 " + translator.t(lang, "employee_private"), callback_data="employee_private")],
        [InlineKeyboardButton(text="❓ " + translator.t(lang, "employee_unknown"), callback_data="employee_unknown")]
    ])
    await msg.answer(translator.t(lang, "pension_title") + "\n\n" + translator.t(lang, "pension_where"), parse_mode="HTML", reply_markup=kb)

@router.callback_query(F.data.startswith("employee_"))
async def employee_chosen(callback: CallbackQuery):
    emp_type = callback.data.split("_")[1]
    uid = callback.from_user.id
    lang = await get_lang(uid)
    user_data[uid] = {"employee_type": emp_type, "step": "age"}

    async with async_session() as session:
        existing = (await session.execute(
            select(PensionProfile).where(PensionProfile.telegram_id == uid)
        )).scalar_one_or_none()
        if existing:
            existing.employee_type = emp_type
            existing.age_now = None
            existing.retirement_age = None
            existing.salary_bruto = None
            existing.seniority_years = None
            existing.contribution_employee = None
            existing.contribution_employer = None
            existing.expected_return = None
            existing.management_fees = None
            existing.result_capital = None
            existing.result_monthly = None
        else:
            profile = PensionProfile(telegram_id=uid, employee_type=emp_type)
            session.add(profile)
        await session.commit()

    await callback.message.answer(translator.t(lang, "pension_age"))
    await callback.answer()

@router.message(F.text.regexp(r'^\d+$'))
async def handle_number(msg: Message):
    uid = msg.from_user.id
    if uid not in user_data:
        return
    lang = await get_lang(uid)
    step = user_data[uid].get("step")
    val = int(msg.text)
    if step == "age":
        user_data[uid]["age_now"] = val
        user_data[uid]["step"] = "retirement_age"
        await msg.answer(translator.t(lang, "pension_retirement"))
    elif step == "retirement_age":
        user_data[uid]["retirement_age"] = val
        user_data[uid]["step"] = "salary"
        await msg.answer(translator.t(lang, "pension_salary"))
    elif step == "salary":
        user_data[uid]["salary_bruto"] = float(val)
        user_data[uid]["step"] = "seniority"
        await msg.answer(translator.t(lang, "pension_seniority"))
    elif step == "seniority":
        user_data[uid]["seniority_years"] = val
        if user_data[uid]["employee_type"] == "public":
            profile = user_data.pop(uid)
            result = calc_budgetary(profile)
            tax = estimate_tax(result["monthly_pension"])
            await msg.answer(
                f"💰 <b>פנסיה תקציבית</b>\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"📆 קצבה: {result['monthly_pension']:,.0f} שח\n"
                f"⚖ מס: {tax:,.0f} שח\n"
                f"📥 נטו: {result['monthly_pension']-tax:,.0f} שח",
                parse_mode="HTML"
            )
        else:
            user_data[uid]["step"] = "contribution_employee"
            await msg.answer(translator.t(lang, "pension_contrib_self"))
    elif step == "contribution_employee":
        user_data[uid]["contribution_employee"] = float(val)
        user_data[uid]["step"] = "contribution_employer"
        await msg.answer(translator.t(lang, "pension_contrib_emp"))
    elif step == "contribution_employer":
        user_data[uid]["contribution_employer"] = float(val)
        user_data[uid]["step"] = "expected_return"
        await msg.answer(translator.t(lang, "pension_return"))
    elif step == "expected_return":
        user_data[uid]["expected_return"] = float(val)
        user_data[uid]["step"] = "management_fees"
        await msg.answer(translator.t(lang, "pension_fees"))
    elif step == "management_fees":
        user_data[uid]["management_fees"] = float(val)
        profile = user_data.pop(uid)
        profile["current_capital"] = 0
        result = calc_accumulating(profile)
        tax = estimate_tax(result["monthly_pension"])
        async with async_session() as session:
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
