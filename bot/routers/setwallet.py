from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select

router = Router()

class WalletState(StatesGroup):
    waiting_for_address = State()

@router.message(Command("setwallet"))
async def cmd_setwallet(msg: Message, state: FSMContext = None):
    # אם יש FSM  נשתמש בו, אחרת נטפל בטקסט ישירות
    if state is not None:
        await msg.answer("📥 שלח את כתובת ארנק ה‑TON שלך (למשל: EQD...):")
        await state.set_state(WalletState.waiting_for_address)
    else:
        # ללא FSM (בדיקות)  פשוט מחזיר הנחיה
        await msg.answer("📥 השתמש בפקודה כדי להגדיר את ארנק ה‑TON שלך.")
