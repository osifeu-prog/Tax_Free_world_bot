from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.keyboards.inline import back_to_start
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("faq"))
async def cmd_faq(msg: Message):
    await msg.answer(MESSAGES["faq"], parse_mode="HTML", reply_markup=back_to_start())

@router.callback_query(F.data == "faq")
async def cb_faq(call: CallbackQuery):
    await call.message.edit_text(MESSAGES["faq"], parse_mode="HTML", reply_markup=back_to_start())
    await call.answer()
