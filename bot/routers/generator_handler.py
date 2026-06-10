from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.tools.generator_multilang import generate_command
router = Router()

@router.message(Command("generate_command"))
async def cmd_generate(msg: Message):
    parts = msg.text.split()
    if len(parts) < 2:
        return await msg.answer("❗ יש לציין שם פקודה: /generate_command mycmd")
    name = parts[1].strip()
    result = generate_command(name)
    await msg.answer(f"✅ {result}")
