from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
router = Router()
@router.message(Command("crypto"))
async def cmd_crypto(msg: Message):
    await msg.answer("₿ מה זה קריפטו? - בקרוב")
