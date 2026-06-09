from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
import random

router = Router()

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else 'he'

@router.message(Command('start'))
async def cmd_start(msg: Message):
    lang = await get_lang(msg.from_user.id)
    name = msg.from_user.first_name or 'חבר'
    tip = random.choice([
        '💡 השווה עמלות לפני כל תשלום  החיסכון השנתי שלך יכול להגיע לאלפי שקלים!',
        '📱 לחץ על מחשבון ויזואלי כדי לראות כמה אתה יכול לחסוך.',
        '🔗 שתף את קוד ההפניה עם חברים וצבור נקודות!',
        '📚 כנס לאקדמיה ולמד איך TON יכולה לשנות את הכלכלה שלך.',
        '🏙️ TON City היא העיר הכלכלית שלך  בדוק /city.'
    ])
    welcome = f'<b>ברוך הבא {name} ל- TON City!</b>\n\nאנחנו פה כדי לעזור לך לחסוך אלפי שקלים בשנה.\n\n{tip}'
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🇮🇱 עברית', callback_data='lang_he'),
         InlineKeyboardButton(text='🇬🇧 English', callback_data='lang_en')],
        [InlineKeyboardButton(text='🇷🇺 Русский', callback_data='lang_ru'),
         InlineKeyboardButton(text='🇸🇦 العربية', callback_data='lang_ar')],
        [InlineKeyboardButton(text='🇪🇸 Español', callback_data='lang_es'),
         InlineKeyboardButton(text='🇫🇷 Français', callback_data='lang_fr')],
        [InlineKeyboardButton(text='🇾🇮 יידיש', callback_data='lang_yi')],
        [InlineKeyboardButton(text='💰 חיסכון', callback_data='go_budget'),
         InlineKeyboardButton(text='📊 פנסיה', callback_data='go_pension')],
        [InlineKeyboardButton(text='🎓 אקדמיה', callback_data='go_academy'),
         InlineKeyboardButton(text='🏙️ TON City', callback_data='go_city')],
        [InlineKeyboardButton(text='💖 תרומה', callback_data='go_donate'),
         InlineKeyboardButton(text='🔗 הפניה', callback_data='go_ref')],
        [InlineKeyboardButton(text='📱 מחשבון ויזואלי', callback_data='open_miniapp')]
    ])
    await msg.answer(welcome, parse_mode='HTML', reply_markup=kb)

@router.callback_query(F.data.startswith('lang_'))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split('_')[1]
    uid = callback.from_user.id
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        if u:
            u.language = lang
        else:
            s.add(User(telegram_id=uid, language=lang))
        await s.commit()
    await callback.message.answer(f'✅ שפה שונתה ל-{lang}')
    await callback.answer()

@router.callback_query(F.data.startswith('go_'))
async def quick_actions(callback: CallbackQuery):
    cmd = callback.data[3:]
    await callback.message.answer(f'/{cmd}')
    await callback.answer()