from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command('whyus'))
async def cmd_whyus(message: Message):
    await message.reply(f"✅ /{r} - הפקודה זמינה (בשלב בנייה)")
    
print(f"✅ Minimal router created: whyus")
