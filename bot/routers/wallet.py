from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
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
        "לחץ לחיבור אוטומטי או הזן ידנית כתובת EQ... / UQ...",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.callback_query(F.data == "manual_wallet")
async def manual_wallet(callback: CallbackQuery):
    await callback.message.answer("📝 שלח את כתובת הארנק שלך:")
    await callback.answer()

@router.message(F.text.startswith("EQ") | F.text.startswith("UQ"))
async def save_wallet(msg: Message):
    address = msg.text.strip()
    if len(address) < 40:
        await msg.answer("❌ כתובת לא תקינה.")
        return
    uid = msg.from_user.id
    async with async_session() as s:
        await s.execute(
            text("UPDATE users SET wallet_address = :addr WHERE telegram_id = :uid"),
            {"addr": address, "uid": uid}
        )
        await s.commit()
    await msg.answer(f"✅ ארנק נשמר:\n`{address}`", parse_mode="Markdown")
