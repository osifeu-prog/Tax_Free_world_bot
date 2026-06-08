from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(Command("donate"))
async def cmd_donate(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 שלח תרומה ב‑TON", url="https://app.tonkeeper.com/transfer/UQCr743gEr_nqV_0SBkSp3CtYS_15R3LDLBvLmKeEv7XdGvp")],
        [InlineKeyboardButton(text="🔗 שתף QR שלך", callback_data="share_qr")]
    ])
    text = """
💖 <b>תמכו בנו!</b>

TON Israel היא קהילה חופשית  ללא מימון ממשלתי.
אם הבוט עוזר לך, תוכל לתרום:

👛 <b>ארנק TON:</b>
<code>UQCr743gEr_nqV_0SBkSp3CtYS_15R3LDLBvLmKeEv7XdGvp</code>

🙏 כל תרומה עוזרת לנו להמשיך לפתח!
"""
    await msg.answer(text, parse_mode="HTML", reply_markup=kb)
