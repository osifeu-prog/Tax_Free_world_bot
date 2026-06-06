from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from bot.keyboards.inline import back_to_main
from bot.messages.he import MESSAGES

router = Router()

@router.message(Command("contact"))
async def cmd_contact(msg: Message):
    await msg.answer(MESSAGES["contact"], parse_mode="HTML", reply_markup=back_to_main())

@router.callback_query(F.data == "contact")
async def show_contact(call: CallbackQuery):
    await call.message.edit_text(MESSAGES["contact"], parse_mode="HTML", reply_markup=back_to_main())
    await call.answer()

