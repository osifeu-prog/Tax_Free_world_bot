from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
router = Router()
WALLET = "UQCr743gEr_nqV_0SBkSp3CtYS_15R3LDLBvLmKeEv7XdGvp"

@router.message(Command('donate'))
async def cmd_donate(msg: Message):
    body = ("💖 <b>תמכו בנו!</b>\n\nTON Israel  קהילה חופשית.\n\n"
            f"👛 ארנק TON:\n<code>{WALLET}</code>\n\n"
            "1️⃣ Tonkeeper → 2️⃣ העבר → 3️⃣ /qr")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💚 50 ', callback_data='donate_50'),
         InlineKeyboardButton(text='💚 100 ', callback_data='donate_100')],
        [InlineKeyboardButton(text='💎 500 ', callback_data='donate_500'),
         InlineKeyboardButton(text='💎 TON', callback_data='donate_ton')],
    ])
    await msg.answer(body, parse_mode='HTML', reply_markup=kb)

@router.callback_query(F.data.startswith('donate_'))
async def donate_handler(callback: CallbackQuery):
    await callback.answer(f'🙏 תודה! ({callback.data.split("_")[1]})', show_alert=True)