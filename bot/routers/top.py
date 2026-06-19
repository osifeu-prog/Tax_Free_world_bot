from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command('top'))
async def cmd_top(message: Message):
    await message.reply(f"✅ /{r} - הפקודה זמינה (בשלב בנייה)")
    
print(f"✅ Minimal router created: top")
