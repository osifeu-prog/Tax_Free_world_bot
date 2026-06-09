# -*- coding: utf-8 -*-
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.keyboards.inline import back_to_main
from bot.messages.he import MESSAGES
from bot.services.referral_service import get_ref_stats, get_top_referrers

router = Router()

@router.message(Command("stats"))
async def cmd_stats(msg: Message):
    users, refs, compares = await get_ref_stats()
    await msg.answer(MESSAGES["stats"].format(users=users, refs=refs, compares=compares), parse_mode="HTML", reply_markup=back_to_main())

@router.message(Command("top"))
async def cmd_top(msg: Message):
    leaders = await get_top_referrers(5)
    await msg.answer(MESSAGES["top_refs"].format(leaders=leaders), parse_mode="HTML", reply_markup=back_to_main())

