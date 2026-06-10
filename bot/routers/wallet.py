from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from sqlalchemy import text

router = Router()

@router.message(Command("setwallet"))
async def cmd_setwallet(msg: Message):
    deep_link = "https://tonkeeper.com/ton-connect"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 חיבור ארנק TON", url=deep_link)],
        [InlineKeyboardButton(text="✏️ הזנה ידנית", callback_data="manual_wallet")]
    ])
    await msg.answer(
        "👛 **חיבור ארנק TON**\n\n"
        "לחץ על הכפתור לחיבור אוטומטי עם Tonkeeper.\n"
        "או בחר הזנה ידנית והדבק את כתובת הארנק שלך.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "manual_wallet")
async def manual_wallet(callback):
    await callback.message.answer("📝 אנא שלח את כתובת הארנק שלך (EQD... או UQD...)")
    await callback.answer()

@router.message()
async def save_wallet(msg: Message):
    address = msg.text.strip()
    if not (address.startswith("EQ") or address.startswith("UQ")):
        return
    uid = msg.from_user.id
    async with async_session() as s:
        await s.execute(text("UPDATE users SET wallet_address = :addr WHERE telegram_id = :uid"), {"addr": address, "uid": uid})
        await s.commit()
    await msg.answer(f"✅ כתובת הארנק נשמרה:\n`{address}`", parse_mode="Markdown")
