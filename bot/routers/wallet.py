# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import CallbackQuery
from bot.keyboards.inline import back_to_main
from bot.messages.he import MESSAGES

router = Router()

@router.callback_query(F.data == "wallet")
async def show_wallet(call: CallbackQuery):
    await call.message.edit_text(MESSAGES["wallet"], parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()

