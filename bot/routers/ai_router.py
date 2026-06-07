from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.ai_service import ask_gemini

router = Router()

@router.message(Command("ai"))
async def cmd_ai(msg: Message):
    question = msg.text.split(maxsplit=1)
    if len(question) == 1:
        await msg.answer("🤖 <b>שימוש:</b> <code>/ai איך לחסוך בעמלות?</code>", parse_mode="HTML")
        return
    await msg.answer("🤖 <i>חושב...</i>", parse_mode="HTML")
    answer = await ask_gemini(question[1])
    await msg.answer(answer)
