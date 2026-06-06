from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from bot.keyboards.inline import back_to_start
from bot.services.profile_service import (
    get_or_create_profile, update_income, add_expense,
    get_expenses, get_total_savings
)

router = Router()

class ProfileForm(StatesGroup):
    waiting_for_income = State()
    waiting_for_expense_category = State()
    waiting_for_expense_amount = State()
    waiting_for_expense_frequency = State()

@router.message(Command("profile"))
async def cmd_profile(msg: Message, state: FSMContext):
    profile = await get_or_create_profile(msg.from_user.id)
    total = await get_total_savings(msg.from_user.id)
    info = f"👤 <b>פרופיל כלכלי</b>\n"
    info += f"💰 הכנסה חודשית: {profile.monthly_income:,.0f}\n"
    info += f"🧮 חיסכון פוטנציאלי ב-TON: {total:,.2f} בשנה\n\n"
    info += "הפקודות:\n"
    info += "/setincome  עדכן הכנסה\n"
    info += "/addexpense  הוסף הוצאה\n"
    info += "/expenses  צפה בהוצאות שלך\n"
    await msg.answer(info, parse_mode="HTML", reply_markup=back_to_start())

@router.message(Command("setincome"))
async def cmd_setincome(msg: Message, state: FSMContext):
    await state.set_state(ProfileForm.waiting_for_income)
    await msg.answer("הזן את ההכנסה החודשית שלך (בש\"ח):")

@router.message(ProfileForm.waiting_for_income)
async def process_income(msg: Message, state: FSMContext):
    try:
        income = float(msg.text)
    except ValueError:
        await msg.answer("מספר לא תקין, נסה שוב.")
        return
    await update_income(msg.from_user.id, income)
    await state.clear()
    await msg.answer(f"✅ ההכנסה עודכנה ל-{income:,.0f}.", reply_markup=back_to_start())

@router.message(Command("addexpense"))
async def cmd_addexpense(msg: Message, state: FSMContext):
    await state.set_state(ProfileForm.waiting_for_expense_category)
    await msg.answer("איזו קטגוריה? (למשל: שכירות, חשמל, ארנונה, סלולר, ביטוח)")

@router.message(ProfileForm.waiting_for_expense_category)
async def process_category(msg: Message, state: FSMContext):
    await state.update_data(category=msg.text)
    await state.set_state(ProfileForm.waiting_for_expense_amount)
    await msg.answer("כמה אתה משלם?")

@router.message(ProfileForm.waiting_for_expense_amount)
async def process_amount(msg: Message, state: FSMContext):
    try:
        amount = float(msg.text)
    except ValueError:
        await msg.answer("מספר לא תקין, נסה שוב.")
        return
    await state.update_data(amount=amount)
    await state.set_state(ProfileForm.waiting_for_expense_frequency)
    await msg.answer("תדירות: חודשי / דו-חודשי / שנתי?")

@router.message(ProfileForm.waiting_for_expense_frequency)
async def process_frequency(msg: Message, state: FSMContext):
    freq = msg.text
    if freq not in ["חודשי", "דו-חודשי", "שנתי"]:
        await msg.answer("אנא הקלד: חודשי, דו-חודשי, או שנתי.")
        return
    data = await state.get_data()
    exp = await add_expense(
        msg.from_user.id,
        data["category"],
        data["amount"],
        freq,
        f"הוסף ע\"י {msg.from_user.first_name}"
    )
    await state.clear()
    await msg.answer(
        f"✅ נוספה הוצאה:\n"
        f"📌 {exp.category}: {exp.amount:,.0f} ({exp.frequency})\n"
        f"💡 חיסכון פוטנציאלי ב-TON: {exp.potential_ton_savings:,.2f} בשנה",
        reply_markup=back_to_start()
    )

@router.message(Command("expenses"))
async def cmd_expenses(msg: Message):
    exps = await get_expenses(msg.from_user.id)
    if not exps:
        await msg.answer("אין לך הוצאות רשומות עדיין. השתמש ב-/addexpense.")
        return
    total = await get_total_savings(msg.from_user.id)
    lines = [f"📌 <b>ההוצאות שלך:</b>"]
    for e in exps:
        lines.append(f"• {e.category}: {e.amount:,.0f} ({e.frequency})  חיסכון TON: {e.potential_ton_savings:,.2f}")
    lines.append(f"\n💰 <b>סה\"כ חיסכון פוטנציאלי: {total:,.2f} בשנה</b>")
    await msg.answer("\n".join(lines), parse_mode="HTML", reply_markup=back_to_start())
