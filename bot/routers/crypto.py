# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("crypto"))
async def cmd_crypto(msg: Message):
    await msg.answer(MESSAGES["crypto"], parse_mode="HTML")

