# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("cbdc"))
async def cmd_cbdc(msg: Message):
    await msg.answer(MESSAGES["cbdc"], parse_mode="HTML")

