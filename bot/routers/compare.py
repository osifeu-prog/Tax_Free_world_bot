from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.services.calculator import build_comparison
from bot.keyboards.inline import presets_menu, back_to_start, share_result
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
        await msg.answer(MESSAGES["compare_usage"], parse_mode="HTML", reply_markup=presets_menu())
        return
    text = build_comparison(amount, tx_per_month)
    await msg.answer(text, parse_mode="HTML", reply_markup=share_result(amount, tx_per_month))

@router.callback_query(F.data == "compare_prompt")
async def compare_prompt(call: CallbackQuery):
    await call.message.edit_text(
        MESSAGES["compare_usage"],
        parse_mode="HTML",
        reply_markup=presets_menu()
    )
    await call.answer()

@router.callback_query(F.data == "presets")
async def show_presets(call: CallbackQuery):
    await call.message.edit_text("בחר תרחיש מוכן:", reply_markup=presets_menu())
    await call.answer()

preset_map = {
    "preset_2500_1": (2500, 1),
    "preset_10000_2": (10000, 2),
    "preset_3000_4": (3000, 4),
    "preset_5000_3": (5000, 3),
}

@router.callback_query(F.data.in_(preset_map.keys()))
async def handle_preset(call: CallbackQuery):
    amount, tx = preset_map[call.data]
    text = build_comparison(amount, tx)
    await call.message.edit_text(text, parse_mode="HTML", reply_markup=share_result(amount, tx))
    await call.answer()
