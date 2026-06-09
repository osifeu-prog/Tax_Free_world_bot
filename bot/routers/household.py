# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from bot.services.profile_service import get_or_create_profile, get_total_savings, get_expenses
from bot.keyboards.inline import back_to_main
from bot.database.models import Household, HouseholdMember, SharedExpense, Chore, ShoppingListItem
from bot.database.session import async_session
from sqlalchemy import select
import random, string

router = Router()

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@router.message(Command("household"))
async def cmd_household(msg: Message):
    parts = msg.text.split()
    if len(parts) < 2:
        await msg.answer(
            "🏠 <b>משק בית  פקודות:</b>\n"
            "/household create  צור משק בית\n"
            "/household invite  הזמן שותף\n"
            "/household join <code>  הצטרף\n"
            "/household stats  סטטיסטיקות\n"
            "/shopping add <item>  הוסף לקניות\n"
            "/shopping list  רשימת קניות\n"
            "/chore add <task>  מטלה\n"
            "/chore list  רשימת מטלות",
            parse_mode="HTML"
        )
        return
    action = parts[1]
    if action == "create":
        async with async_session() as session:
            code = generate_code()
            h = Household(code=code, creator_id=msg.from_user.id)
            session.add(h)
            await session.commit()
            # add creator as member
            session.add(HouseholdMember(household_id=h.id, telegram_id=msg.from_user.id))
            await session.commit()
            await msg.answer(f"🏠 משק הבית נוצר! הקוד להזמנה: <code>{code}</code>", parse_mode="HTML")
    elif action == "join":
        if len(parts) < 3:
            await msg.answer("השתמש: <code>/household join <code></code>", parse_mode="HTML")
            return
        code = parts[2]
        async with async_session() as session:
            result = await session.execute(select(Household).where(Household.code == code))
            h = result.scalar_one_or_none()
            if not h:
                await msg.answer("קוד לא נמצא.")
                return
            # check if already member
            existing = await session.execute(select(HouseholdMember).where(HouseholdMember.household_id == h.id, HouseholdMember.telegram_id == msg.from_user.id))
            if existing.scalar_one_or_none():
                await msg.answer("אתה כבר חבר במשק הבית הזה.")
                return
            session.add(HouseholdMember(household_id=h.id, telegram_id=msg.from_user.id))
            await session.commit()
            await msg.answer("✅ הצטרפת למשק הבית!")
    elif action == "stats":
        # show household stats
        async with async_session() as session:
            member = await session.execute(select(HouseholdMember).where(HouseholdMember.telegram_id == msg.from_user.id))
            member = member.scalar_one_or_none()
            if not member:
                await msg.answer("אינך חבר במשק בית.")
                return
            # count members, expenses, chores, shopping items
            members = await session.execute(select(HouseholdMember).where(HouseholdMember.household_id == member.household_id))
            member_count = len(members.scalars().all())
            expenses = await session.execute(select(SharedExpense).where(SharedExpense.household_id == member.household_id))
            expense_count = len(expenses.scalars().all())
            chores = await session.execute(select(Chore).where(Chore.household_id == member.household_id))
            chore_count = len(chores.scalars().all())
            items = await session.execute(select(ShoppingListItem).where(ShoppingListItem.household_id == member.household_id))
            item_count = len(items.scalars().all())
            await msg.answer(
                f"🏠 <b>משק הבית</b>\n"
                f"👥 חברים: {member_count}\n"
                f"📊 הוצאות: {expense_count}\n"
                f"✅ מטלות: {chore_count}\n"
                f"🛒 פריטי קנייה: {item_count}",
                parse_mode="HTML"
            )

@router.message(Command("shopping"))
async def cmd_shopping(msg: Message):
    parts = msg.text.split(maxsplit=2)
    if len(parts) < 2:
        await msg.answer("השתמש: <code>/shopping add <item></code> או <code>/shopping list</code>", parse_mode="HTML")
        return
    action = parts[1]
    if action == "add":
        if len(parts) < 3:
            await msg.answer("השתמש: <code>/shopping add <item></code>", parse_mode="HTML")
            return
        item = parts[2]
        async with async_session() as session:
            member = await session.execute(select(HouseholdMember).where(HouseholdMember.telegram_id == msg.from_user.id))
            member = member.scalar_one_or_none()
            if not member:
                await msg.answer("אינך חבר במשק בית. צור או הצטרף עם /household.")
                return
            session.add(ShoppingListItem(household_id=member.household_id, added_by=msg.from_user.id, item=item))
            await session.commit()
            await msg.answer(f"🛒 {item} נוסף לרשימת הקניות!")
    elif action == "list":
        async with async_session() as session:
            member = await session.execute(select(HouseholdMember).where(HouseholdMember.telegram_id == msg.from_user.id))
            member = member.scalar_one_or_none()
            if not member:
                await msg.answer("אינך חבר במשק בית.")
                return
            items = await session.execute(select(ShoppingListItem).where(ShoppingListItem.household_id == member.household_id))
            items = items.scalars().all()
            if not items:
                await msg.answer("הרשימה ריקה.")
                return
            lst = "\n".join(f"{'✅' if i.bought else '⬜'} {i.item}" for i in items)
            await msg.answer(f"🛒 <b>רשימת קניות:</b>\n{lst}", parse_mode="HTML")

@router.message(Command("chore"))
async def cmd_chore(msg: Message):
    parts = msg.text.split(maxsplit=2)
    if len(parts) < 2:
        await msg.answer("השתמש: <code>/chore add <task></code> או <code>/chore list</code>", parse_mode="HTML")
        return
    action = parts[1]
    if action == "add":
        if len(parts) < 3:
            await msg.answer("השתמש: <code>/chore add <task></code>", parse_mode="HTML")
            return
        task = parts[2]
        async with async_session() as session:
            member = await session.execute(select(HouseholdMember).where(HouseholdMember.telegram_id == msg.from_user.id))
            member = member.scalar_one_or_none()
            if not member:
                await msg.answer("אינך חבר במשק בית.")
                return
            session.add(Chore(household_id=member.household_id, assigned_to=msg.from_user.id, title=task))
            await session.commit()
            await msg.answer(f"✅ המטלה '{task}' נוספה!")
    elif action == "list":
        async with async_session() as session:
            member = await session.execute(select(HouseholdMember).where(HouseholdMember.telegram_id == msg.from_user.id))
            member = member.scalar_one_or_none()
            if not member:
                await msg.answer("אינך חבר במשק בית.")
                return
            chores = await session.execute(select(Chore).where(Chore.household_id == member.household_id))
            chores = chores.scalars().all()
            if not chores:
                await msg.answer("אין מטלות.")
                return
            lst = "\n".join(f"{'✅' if c.done else '⬜'} {c.title}" for c in chores)
            await msg.answer(f"📋 <b>מטלות:</b>\n{lst}", parse_mode="HTML")

