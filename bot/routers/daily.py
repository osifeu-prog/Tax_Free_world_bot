# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.referral_service import get_ref_stats, get_top_referrers
from bot.services.profile_service import get_total_users_with_expenses, get_total_savings_sum
from bot.keyboards.inline import back_to_main
from datetime import datetime

router = Router()

async def daily_handler(msg: Message):
    users, refs, compares = await get_ref_stats()
    expense_users = await get_total_users_with_expenses()
    total_savings = await get_total_savings_sum()
    top = await get_top_referrers(3)
    text = (
        f"📈 <b>סיכום יומי  {datetime.now().strftime('%d/%m/%Y')}</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👥 משתמשים ייחודיים: <b>{users}</b>\n"
        f"🔗 הפניות: <b>{refs}</b>\n"
        f"🧮 חיפושים במחשבון: <b>{compares}</b>\n"
        f"🏠 משתמשים שמנהלים תקציב: <b>{expense_users}</b>\n"
        f"💰 סך חיסכון פוטנציאלי: <b>{total_savings:,.2f}</b>\n\n"
        f"🏆 <b>מובילים:</b>\n{top}\n\n"
        f"📱 מחשבון ויזואלי: /miniapp"
    )
    await msg.answer(text, parse_mode="HTML", reply_markup=back_to_main())

@router.message(Command("daily"))
async def cmd_daily(msg: Message):
    await daily_handler(msg)

