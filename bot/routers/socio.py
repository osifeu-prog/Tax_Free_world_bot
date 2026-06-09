# -*- coding: utf-8 -*-
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("socio"))
async def cmd_socio(msg: Message):
    await msg.answer(MESSAGES["socio"], parse_mode="HTML")

