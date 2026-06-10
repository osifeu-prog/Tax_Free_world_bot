# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.keyboards.inline import back_to_main
from bot.messages.he import MESSAGES
from bot.services.referral_service import get_or_create_ref_code

router = Router()

@router.message(Command("ref"))
async def cmd_ref(msg: Message):
    code = await get_or_create_ref_code(msg.from_user.id)
    await msg.answer(MESSAGES["ref_intro"].format(ref_code=code), parse_mode="HTML", reply_markup=back_to_main())

@router.callback_query(F.data == "my_ref")
async def my_ref(call: CallbackQuery):
    code = await get_or_create_ref_code(call.from_user.id)
    await call.message.edit_text(MESSAGES["ref_intro"].format(ref_code=code), parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()



