# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.keyboards.inline import back_to_main
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("faq"))
async def cmd_faq(msg: Message):
    await msg.answer(MESSAGES["faq"], parse_mode="HTML", reply_markup=back_to_main())

@router.callback_query(F.data == "faq")
async def cb_faq(call: CallbackQuery):
    await call.message.edit_text(MESSAGES["faq"], parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()


