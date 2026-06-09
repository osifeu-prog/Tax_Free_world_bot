from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
router = Router()

@router.message(Command('donate'))
async def cmd_donate(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💚 50 ', callback_data='donate_50'),
         InlineKeyboardButton(text='💚 100 ', callback_data='donate_100')],
        [InlineKeyboardButton(text='💎 500 ', callback_data='donate_500'),
         InlineKeyboardButton(text='💎 TON', callback_data='donate_ton')],
        [InlineKeyboardButton(text='🔗 שתף עם חברים', switch_inline_query='תרום ל-TON Israel!')]
    ])
    await msg.answer(
        '<b>💖 תמכו בנו!</b>\n\n'
        'TON Israel היא קהילה חופשית ללא מימון ממשלתי.\n'
        'התרומה שלך עוזרת לנו להמשיך לפתח.\n\n'
        '👛 ארנק TON:\n<code>UQCr743gEr_nqV_0SBkSp3CtYS_15R3LDLBvLmKeEv7XdGvp</code>\n\n'
        'ℹ️ איך לתרום?\n'
        '1️⃣ פתח ארנק TON (Tonkeeper, Tonhub).\n'
        '2️⃣ העבר סכום לכתובת למעלה.\n'
        '3️⃣ שלח /qr לקבלת קוד QR לשיתוף.\n\n'
        '🙏 כל תרומה עוזרת!',
        parse_mode='HTML', reply_markup=kb
    )

@router.callback_query(F.data.startswith('donate_'))
async def donate_handler(callback: CallbackQuery):
    amount = callback.data.split('_')[1]
    await callback.answer(f'🙏 תודה על התמיכה! ({amount})', show_alert=True)
