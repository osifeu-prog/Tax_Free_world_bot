from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select, text
from bot.database.session import engine

router = Router()

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else 'he'

@router.message(Command('donate'))
async def cmd_donate(msg: Message):
    lang = await get_lang(msg.from_user.id)
    try:
        from bot.services.translation_service import translator
        title = translator.t(lang, 'donate_title')
        body = translator.t(lang, 'donate_text')
        btn50 = translator.t(lang, 'donate_50')
        btn100 = translator.t(lang, 'donate_100')
        btn500 = translator.t(lang, 'donate_500')
        btnTON = translator.t(lang, 'donate_ton')
    except:
        title, body = '💖 תמכו בנו!', 'הקהילה חופשית  תרומתך עוזרת.'
        btn50, btn100, btn500, btnTON = '50 ', '100 ', '500 ', 'TON'

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn50, callback_data='donate_50'), InlineKeyboardButton(text=btn100, callback_data='donate_100')],
        [InlineKeyboardButton(text=btn500, callback_data='donate_500'), InlineKeyboardButton(text=btnTON, callback_data='donate_ton')],
        [InlineKeyboardButton(text='🔗 שתף עם חברים', switch_inline_query='תרום ל-TON Israel!')]
    ])
    await msg.answer(f'<b>{title}</b>\n\n{body}', parse_mode='HTML', reply_markup=kb)

@router.callback_query(F.data.startswith('donate_'))
async def donate_handler(callback: CallbackQuery):
    amount = callback.data.split('_')[1]
    uid = callback.from_user.id
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda c: c.execute(text("INSERT INTO donations (user_id, amount) VALUES (:uid, :amt)"), {"uid": uid, "amt": amount}))
    except: pass
    await callback.answer(f'🙏 תודה על התמיכה! ({amount})', show_alert=True)