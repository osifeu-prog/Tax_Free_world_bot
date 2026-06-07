from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.ai_service import ask_ai

router = Router()

@router.message(Command("ai"))
async def cmd_ai(msg: Message):
    question = msg.text.split(maxsplit=1)
    if len(question) == 1:
        await msg.answer("🤖 <b>שימוש:</b> <code>/ai איך לחסוך בעמלות?</code>", parse_mode="HTML")
        return
    await msg.answer("🤖 <i>חושב...</i>", parse_mode="HTML")
    answer = await ask_ai(question[1])
    await msg.answer(answer)

@router.message(Command("architecture"))
async def cmd_architecture(msg: Message):
    diagram = '''
<b>🏗️ ארכיטקטורת TON Israel Bot</b>
━━━━━━━━━━━━━━━━━━━━━━━
משתמש ←→ Telegram Bot ←→ aiogram Dispatcher
                ↓
        ┌───────┴────────┐
        │   47 Routers     │
        │ (פקודות + FSM)   │
        └───────┬────────┘
                ↓
        ┌───────┴────────┐
        │   Services       │
        │ (AI, Points,     │
        │  RBAC, Profile)  │
        └───────┬────────┘
                ↓
        ┌───────┴────────┐
        │   Database       │
        │ (PostgreSQL)     │
        └────────────────┘
━━━━━━━━━━━━━━━━━━━━━━━
🧠 AI: Groq → Gemini (fallback)
📦 Redis: מטמון
🔐 RBAC: הרשאות מבוססות תפקידים
📊 Analytics: /stats, /daily, /household
    '''
    await msg.answer(diagram, parse_mode="HTML")
