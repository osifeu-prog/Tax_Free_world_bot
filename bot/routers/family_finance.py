from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from bot.database.session import async_session
from bot.database.models import UserProfile, UserExpense
from sqlalchemy import select
from bot.services.family_calc import add_income, add_expense, calculate_savings
import json

router = Router()

@router.message(Command("setincome"))
async def cmd_setincome(msg: Message):
    parts = msg.text.split()
    if len(parts) < 2:
        await msg.answer("השתמש: /setincome <סכום>")
        return
    amount = float(parts[1])
    async with async_session() as session:
        stmt = select(UserProfile).where(UserProfile.telegram_id == msg.from_user.id)
        profile = (await session.execute(stmt)).scalar_one_or_none()
        if not profile:
            profile = UserProfile(telegram_id=msg.from_user.id, monthly_income=amount)
            session.add(profile)
        else:
            profile.monthly_income = amount
        await session.commit()
    await msg.answer(f"✅ ההכנסה החודשית עודכנה ל‑{amount:,.0f} שח")

@router.message(Command("addexpense"))
async def cmd_addexpense(msg: Message):
    parts = msg.text.split(maxsplit=2)
    if len(parts) < 3:
        await msg.answer("השתמש: /addexpense <קטגוריה> <סכום>")
        return
    category = parts[1]
    try:
        amount = float(parts[2])
    except:
        await msg.answer("סכום לא תקין")
        return
    async with async_session() as session:
        expense = UserExpense(telegram_id=msg.from_user.id, category=category, amount=amount, frequency="חודשי")
        session.add(expense)
        await session.commit()
    await msg.answer(f"✅ הוצאה '{category}' בסך {amount:,.0f} שח נוספה")

@router.message(Command("mysavings"))
async def cmd_mysavings(msg: Message):
    async with async_session() as session:
        profile = (await session.execute(select(UserProfile).where(UserProfile.telegram_id == msg.from_user.id))).scalar_one_or_none()
        if not profile or not profile.monthly_income:
            await msg.answer("תחילה הגדר הכנסה: /setincome")
            return
        expenses = (await session.execute(select(UserExpense).where(UserExpense.telegram_id == msg.from_user.id))).scalars().all()
        income = profile.monthly_income
        savings = calculate_savings(income, [{"amount": e.amount} for e in expenses])
        total_exp = sum(e.amount for e in expenses)
        await msg.answer(
            f"💰 <b>סיכום חודשי</b>\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"📥 הכנסה: {income:,.0f} שח\n"
            f"📤 הוצאות: {total_exp:,.0f} שח\n"
            f"💚 חיסכון: {savings:,.0f} שח",
            parse_mode="HTML"
        )
