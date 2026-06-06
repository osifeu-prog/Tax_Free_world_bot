from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from bot.keyboards.inline import start_menu, back_to_start, academy_menu
from bot.messages.he import MESSAGES
from bot.services.referral_service import get_ref_stats, get_top_referrers
import random

router = Router()

def greet(name):
    return MESSAGES["start"].replace("{user}", name)

@router.message(Command("start"))
async def cmd_start(msg: Message, command: CommandObject):
    name = msg.from_user.first_name
    args = command.args
    if args and args.startswith("ref"):
        code = args[3:]
        text = MESSAGES["ref_landing"].format(referrer=code, start_message=greet(name))
    else:
        text = greet(name)
    await msg.answer(text, parse_mode="HTML", reply_markup=start_menu())

@router.callback_query(F.data == "start")
async def back_to_start_cb(call: CallbackQuery):
    name = call.from_user.first_name
    await call.message.edit_text(greet(name), parse_mode="HTML", reply_markup=start_menu())
    await call.answer()

@router.callback_query(F.data == "academy")
async def show_academy(call: CallbackQuery):
    await call.message.edit_text("📚 <b>אקדמיה  בחר נושא:</b>", parse_mode="HTML", reply_markup=academy_menu())
    await call.answer()

# Callbacks לנושאי האקדמיה
for topic in ["crypto", "cbdc", "decentral", "socio", "anti", "edu"]:
    @router.callback_query(F.data == topic)
    async def topic_handler(call: CallbackQuery, t=topic):
        await call.message.edit_text(MESSAGES[t], parse_mode="HTML", reply_markup=back_to_start())
        await call.answer()

# Callback ללוח מובילים
@router.callback_query(F.data == "top")
async def show_top(call: CallbackQuery):
    leaders = await get_top_referrers(5)
    text = MESSAGES["top_refs"].format(leaders=leaders)
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_start())
    await call.answer()

# Callback לסטטיסטיקות
@router.callback_query(F.data == "stats")
async def show_stats(call: CallbackQuery):
    users, refs, compares = await get_ref_stats()
    text = MESSAGES["stats"].format(users=users, refs=refs, compares=compares)
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=back_to_start())
    await call.answer()

# Callback למחשבון תקציב
@router.callback_query(F.data == "budget_prompt")
async def budget_prompt(call: CallbackQuery):
    await call.message.edit_text(
        "השתמש בפקודה: <code>/budget <הכנסה חודשית></code>\nלדוגמה: <code>/budget 12000</code>",
        parse_mode="HTML",
        reply_markup=back_to_start()
    )
    await call.answer()

# Callback לטיפ
@router.callback_query(F.data == "tip")
async def show_tip(call: CallbackQuery):
    tip_text = random.choice(MESSAGES["tips"])
    await call.message.edit_text(MESSAGES["tip"].format(tip_text=tip_text), parse_mode="HTML", reply_markup=back_to_start())
    await call.answer()
