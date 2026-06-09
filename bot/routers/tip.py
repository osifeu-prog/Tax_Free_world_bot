# -*- coding: utf-8 -*-
import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.keyboards.inline import back_to_main
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("tip"))
async def cmd_tip(msg: Message):
    tip_text = random.choice(MESSAGES["tips"])
    await msg.answer(MESSAGES["tip"].format(tip_text=tip_text), parse_mode="HTML", reply_markup=back_to_main())

@router.callback_query(F.data == "tip")
async def cb_tip(call: CallbackQuery):
    tip_text = random.choice(MESSAGES["tips"])
    await call.message.edit_text(MESSAGES["tip"].format(tip_text=tip_text), parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()


