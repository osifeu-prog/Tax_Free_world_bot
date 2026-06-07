from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.profile_service import get_or_create_profile, get_total_savings, get_expenses
from bot.keyboards.inline import back_to_main

router = Router()

@router.message(Command("household"))
async def cmd_household(msg: Message):
    profile = await get_or_create_profile(msg.from_user.id)
    total = await get_total_savings(msg.from_user.id)
    exps = await get_expenses(msg.from_user.id)
    if not exps:
        await msg.answer("אין לך הוצאות עדיין. שלח /addexpense להוספה.")
        return
    lines = [
        "🏠 <b>דשבורד כלכלת הבית</b>",
        f"💰 הכנסה חודשית: {profile.monthly_income:,.0f}",
        f"🧮 חיסכון פוטנציאלי: {total:,.2f}",
        "━━━━━━━━━━━━━━━━",
        "📊 <b>ההוצאות:</b>"
    ]
    for e in exps[:5]:
        lines.append(f"• {e.category}: {e.amount:,.0f} ({e.frequency})  חיסכון TON: {e.potential_ton_savings:,.2f}")
    lines.append(f"\n💰 <b>סה\"כ חיסכון פוטנציאלי: {total:,.2f} בשנה</b>")
    await msg.answer("\n".join(lines), parse_mode="HTML", reply_markup=back_to_main())
