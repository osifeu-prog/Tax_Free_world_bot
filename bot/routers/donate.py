from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.event_logger import log_event

router = Router()

@router.message(Command("donate"))
async def cmd_donate(msg: Message):
    await msg.answer(
        "💖 <b>תמכו בנו!</b>\n\n"
        "TON Israel היא קהילה חופשית ללא מימון ממשלתי.\n"
        "אם הבוט עוזר לך, תוכל לתרום:\n\n"
        "👛 <b>ארנק TON:</b>\n"
        "UQCr743gEr_nqV_0SBkSp3CtYS_15R3LDLBvLmKeEv7XdGvp\n\n"
        "ℹ️ <b>איך לתרום?</b>\n"
        "1️⃣ פתח ארנק TON (Tonkeeper, Tonhub).\n"
        "2️⃣ העבר סכום לכתובת למעלה.\n"
        "3️⃣ שלח /qr לקבלת קוד QR לשיתוף.\n\n"
        "🙏 כל תרומה עוזרת לנו להמשיך לפתח!",
        parse_mode="HTML"
    )
    await log_event(msg.from_user.id, "donate_view")
