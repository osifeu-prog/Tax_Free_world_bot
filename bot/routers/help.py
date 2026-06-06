from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.keyboards.inline import back_to_start
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer(MESSAGES["help"], parse_mode="HTML")

@router.callback_query(F.data == "help")
async def help_cb(call: CallbackQuery):
    await call.message.edit_text(MESSAGES["help"], parse_mode="HTML", reply_markup=back_to_start())
    await call.answer()
