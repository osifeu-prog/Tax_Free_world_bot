# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from bot.keyboards.inline import back_to_main
from bot.services.profile_service import (
    get_or_create_profile, update_income, add_expense,
    get_expenses, get_total_savings, delete_expense
)

router = Router()

class ProfileForm(StatesGroup):
    waiting_for_income = State()
    waiting_for_expense_category = State()
    waiting_for_expense_amount = State()
    waiting_for_expense_frequency = State()

@router.message(Command("profile"))
async def cmd_profile(msg: Message):
    profile = await get_or_create_profile(msg.from_user.id)
    total = await get_total_savings(msg.from_user.id)
    info = (
        f"👤 <b>פרופיל כלכלי</b>\n"
        f"💰 הכנסה חודשית: {profile.monthly_income:,.0f}\n"
        f"🧮 חיסכון פוטנציאלי: {total:,.2f} בשנה\n\n"
        f"/setincome  עדכן הכנסה\n"
        f"/addexpense  הוסף הוצאה\n"
        f"/expenses  צפה בהוצאות\n"
        f"/delexpense  מחק הוצאה"
    )
    await msg.answer(info, parse_mode="HTML", reply_markup=back_to_main())

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
    await msg.answer(f"✅ ההכנסה עודכנה ל-{income:,.0f}.", reply_markup=back_to_main())

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
    exp = await add_expense(msg.from_user.id, data["category"], data["amount"], freq)
    await state.clear()
    await msg.answer(
        f"✅ נוספה הוצאה:\n"
        f"📌 {exp.category}: {exp.amount:,.0f} ({exp.frequency})\n"
        f"💡 חיסכון פוטנציאלי: {exp.potential_ton_savings:,.2f} בשנה",
        reply_markup=back_to_main()
    )

@router.message(Command("expenses"))
async def cmd_expenses(msg: Message):
    exps = await get_expenses(msg.from_user.id)
    if not exps:
        await msg.answer("אין לך הוצאות עדיין. שלח /addexpense להוספה.")
        return
    total = await get_total_savings(msg.from_user.id)
    lines = [f"📌 <b>ההוצאות שלך:</b>"]
    for e in exps:
        lines.append(f"• {e.category}: {e.amount:,.0f} ({e.frequency})  ID: {e.id}")
    lines.append(f"\n💰 <b>סה\"כ חיסכון: {total:,.2f} בשנה</b>")
    lines.append("\nלמחיקת הוצאה: /delexpense <ID>")
    await msg.answer("\n".join(lines), parse_mode="HTML", reply_markup=back_to_main())

@router.message(Command("delexpense"))
async def cmd_delexpense(msg: Message):
    parts = msg.text.split()
    if len(parts) < 2:
        await msg.answer("שימוש: /delexpense <ID>\nלדוגמה: /delexpense 3")
        return
    try:
        expense_id = int(parts[1])
    except ValueError:
        await msg.answer("ID לא תקין.")
        return
    deleted = await delete_expense(msg.from_user.id, expense_id)
    if deleted:
        await msg.answer("✅ ההוצאה נמחקה.", reply_markup=back_to_main())
    else:
        await msg.answer("⛔ לא נמצאה הוצאה או שאין הרשאה.", reply_markup=back_to_main())

