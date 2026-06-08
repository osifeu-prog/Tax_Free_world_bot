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
async def cmd_setwallet(msg: Message, state: FSMContext):
    await msg.answer("📥 שלח את כתובת ארנק ה‑TON שלך (למשל: EQD...):")
    await state.set_state(WalletState.waiting_for_address)

@router.message(WalletState.waiting_for_address)
async def save_wallet(msg: Message, state: FSMContext):
    address = msg.text.strip()
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == msg.from_user.id))).scalar_one_or_none()
        if u:
            u.wallet_address = address
        else:
            u = User(telegram_id=msg.from_user.id, wallet_address=address, language="he")
            s.add(u)
        await s.commit()
    await msg.answer(f"✅ ארנק TON נשמר:\n<code>{address}</code>", parse_mode="HTML")
    await state.clear()
