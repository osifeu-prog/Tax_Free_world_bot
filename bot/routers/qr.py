from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from bot.services.event_logger import log_event
import qrcode
from io import BytesIO

router = Router()

@router.message(Command("qr"))
async def cmd_qr(msg: Message):
    user_id = msg.from_user.id
    deep_link = f"https://t.me/Tax_Free_world_bot?start=ref{user_id}"
    img = qrcode.make(deep_link)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    await msg.answer_photo(
        photo=BufferedInputFile(buf.read(), filename="qr.png"),
        caption=f"🔗 קישור ההפניה שלך:\n{deep_link}\n\nשלם ב‑TON, Bitcoin, USDT!"
    )
    await log_event(user_id, "qr_view")
