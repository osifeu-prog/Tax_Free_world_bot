from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.messages.he import MESSAGES
from bot.keyboards.inline import back_to_main

router = Router()

@router.message(Command("academy_extended"))
async def cmd_academy_extended(msg: Message):
    await msg.answer(MESSAGES["academy_extended"], parse_mode="HTML", reply_markup=back_to_main())

@router.message(Command("academy_nft"))
async def cmd_academy_nft(msg: Message):
    await msg.answer(MESSAGES["academy_nft"], parse_mode="HTML", reply_markup=back_to_main())

@router.message(Command("academy_dao"))
async def cmd_academy_dao(msg: Message):
    await msg.answer(MESSAGES["academy_dao"], parse_mode="HTML", reply_markup=back_to_main())
