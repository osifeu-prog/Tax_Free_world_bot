# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandObject
from bot.keyboards.inline import main_menu, back_to_main, savings_menu, household_menu, academy_menu, community_menu
from bot.messages.he import MESSAGES
from bot.services.referral_service import get_ref_stats, get_top_referrers, register_user
from bot.services.profile_service import get_or_create_profile, get_total_savings, get_expenses
import random

router = Router()

reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 חיסכון"), KeyboardButton(text="🏠 כלכלת הבית")],
        [KeyboardButton(text="📚 אקדמיה"), KeyboardButton(text="👥 קהילה")],
        [KeyboardButton(text="📱 מחשבון ויזואלי"), KeyboardButton(text="📈 סיכום יומי")],
        [KeyboardButton(text="📝 פידבק"), KeyboardButton(text="ℹ️ עזרה")],
    ],
    resize_keyboard=True
)

def greet(name):
    return MESSAGES["start"].replace("{user}", name)

@router.message(Command("start"))
async def cmd_start(msg: Message, command: CommandObject):
    await register_user(msg.from_user.id)
    name = msg.from_user.first_name
    args = command.args
    if args and args.startswith("ref"):
        code = args[3:]
        text = MESSAGES["ref_landing"].format(referrer=code, start_message=greet(name))
        await msg.answer(text, parse_mode="HTML", reply_markup=main_menu())
    else:
        await msg.answer(greet(name), parse_mode="HTML", reply_markup=main_menu())
    # הסבר מיני-אפ
    await msg.answer(
        "💡 <b>טיפ:</b> לחץ על הכפתור הכחול 📱 <b>בפינה השמאלית התחתונה</b> כדי לפתוח את המחשבון הוויזואלי!",
        parse_mode="HTML"
    )
    await msg.answer("ניווט מהיר:", reply_markup=reply_kb)

@router.callback_query(F.data == "start")
async def back_to_main_cb(call: CallbackQuery):
    name = call.from_user.first_name
    await call.message.edit_text(greet(name), parse_mode="HTML", reply_markup=main_menu())
    await call.answer()

@router.callback_query(F.data == "menu_savings")
async def show_savings(call: CallbackQuery):
    await call.message.edit_text("💰 <b>חיסכון ועמלות  בחר:</b>", parse_mode="HTML", reply_markup=savings_menu())
    await call.answer()

@router.callback_query(F.data == "menu_household")
async def show_household(call: CallbackQuery):
    await call.message.edit_text("🏠 <b>ניהול כלכלת הבית  בחר:</b>", parse_mode="HTML", reply_markup=household_menu())
    await call.answer()

@router.callback_query(F.data == "menu_academy")
async def show_academy(call: CallbackQuery):
    await call.message.edit_text("📚 <b>אקדמיה  בחר נושא:</b>", parse_mode="HTML", reply_markup=academy_menu())
    await call.answer()

@router.callback_query(F.data == "menu_community")
async def show_community(call: CallbackQuery):
    await call.message.edit_text("👥 <b>קהילה וכלים  בחר:</b>", parse_mode="HTML", reply_markup=community_menu())
    await call.answer()

# Generic topic callbacks
TOPICS = ["crypto", "cbdc", "decentral", "socio", "anti", "edu", "faq", "academy_nft", "academy_dao", "academy_extended"]
for topic in TOPICS:
    @router.callback_query(F.data == topic)
    async def topic_handler(call: CallbackQuery, t=topic):
        await call.message.edit_text(MESSAGES[t], parse_mode="HTML", reply_markup=back_to_main())
        await call.answer()

@router.callback_query(F.data == "top")
async def show_top(call: CallbackQuery):
    leaders = await get_top_referrers(5)
    text = MESSAGES["top_refs"].format(leaders=leaders)
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()

@router.callback_query(F.data == "stats")
async def show_stats(call: CallbackQuery):
    users, refs, compares = await get_ref_stats()
    text = MESSAGES["stats"].format(users=users, refs=refs, compares=compares)
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()

@router.callback_query(F.data == "tip")
async def show_tip(call: CallbackQuery):
    tip_text = random.choice(MESSAGES["tips"])
    await call.message.edit_text(MESSAGES["tip"].format(tip_text=tip_text), parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()

@router.callback_query(F.data == "help")
async def show_help(call: CallbackQuery):
    await call.message.edit_text(MESSAGES["help"], parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()

@router.callback_query(F.data == "budget_prompt")
async def budget_prompt(call: CallbackQuery):
    await call.message.edit_text(
        "השתמש בפקודה:\n<code>/budget 12000</code>\n(החלף 12000 בהכנסה שלך)",
        parse_mode="HTML",
        reply_markup=back_to_main()
    )
    await call.answer()

@router.callback_query(F.data == "profile")
async def show_profile(call: CallbackQuery):
    profile = await get_or_create_profile(call.from_user.id)
    total = await get_total_savings(call.from_user.id)
    info = (
        f"👤 <b>פרופיל כלכלי</b>\n"
        f"💰 הכנסה חודשית: {profile.monthly_income:,.0f}\n"
        f"🧮 חיסכון פוטנציאלי: {total:,.2f} בשנה\n\n"
        f"לעדכון הכנסה: /setincome\n"
        f"להוספת הוצאה: /addexpense\n"
        f"לצפייה בהוצאות: /expenses"
    )
    await call.message.edit_text(info, parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()

@router.callback_query(F.data == "expenses")
async def show_expenses(call: CallbackQuery):
    exps = await get_expenses(call.from_user.id)
    if not exps:
        await call.message.edit_text("אין לך הוצאות עדיין.", reply_markup=back_to_main())
        await call.answer()
        return
    total = await get_total_savings(call.from_user.id)
    lines = [f"📌 <b>ההוצאות שלך:</b>"]
    for e in exps:
        lines.append(f"• {e.category}: {e.amount:,.0f} ({e.frequency})  חיסכון TON: {e.potential_ton_savings:,.2f}")
    lines.append(f"\n💰 <b>סה\"כ חיסכון: {total:,.2f} בשנה</b>")
    await call.message.edit_text("\n".join(lines), parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()

@router.callback_query(F.data == "donate")
async def show_donate(call: CallbackQuery):
    from bot.routers.donate import cmd_donate
    await cmd_donate(call.message, None)
    await call.answer()

@router.callback_query(F.data == "contact")
async def show_contact(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 שלח הודעה ל-SPARK", url="https://t.me/+1ANn25HeVBoxNmRk")],
        [InlineKeyboardButton(text="🔙 חזרה", callback_data="start")],
    ])
    await call.message.edit_text(
        "📬 <b>צור קשר</b>\n\nאפשר לפנות אלינו ישירות:",
        parse_mode="HTML",
        reply_markup=kb
    )
    await call.answer()

# Callbacks for ask, feedback, roadmap, communities, gift
@router.callback_query(F.data == "ask")
async def prompt_ask(call: CallbackQuery):
    await call.message.edit_text(MESSAGES["ask_prompt"], parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()

@router.callback_query(F.data == "feedback")
async def prompt_feedback(call: CallbackQuery):
    await call.message.edit_text(MESSAGES["feedback_prompt"], parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()

@router.callback_query(F.data == "roadmap")
async def show_roadmap(call: CallbackQuery):
    await call.message.edit_text(MESSAGES["roadmap"], parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()

@router.callback_query(F.data == "communities")
async def show_communities(call: CallbackQuery):
    await call.message.edit_text(MESSAGES["communities"], parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()

@router.callback_query(F.data == "gift")
async def show_gift(call: CallbackQuery):
    from bot.routers.gift import cmd_gift
    # We need a fake message object  using call.message for simplicity
    await cmd_gift(call.message)
    await call.answer()


