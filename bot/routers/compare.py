from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.services.calculator import build_comparison
from bot.keyboards.inline import back_to_start
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("compare"))
async def cmd_compare(msg: Message):
    parts = msg.text.split()
    amount = 500.0
    tx_per_month = 10
    try:
        if len(parts) >= 2:
            amount = float(parts[1])
        if len(parts) >= 3:
            tx_per_month = int(parts[2])
    except ValueError:
        await msg.answer(MESSAGES["compare_usage"], parse_mode="HTML")
        return
    await msg.answer(build_comparison(amount, tx_per_month), parse_mode="HTML")

@router.callback_query(F.data == "compare_prompt")
async def compare_prompt(call: CallbackQuery):
    await call.message.edit_text(
        MESSAGES["compare_usage"] + "\n\n" + MESSAGES["calc_help"],
        parse_mode="HTML",
        reply_markup=back_to_start()
    )
    await call.answer()
