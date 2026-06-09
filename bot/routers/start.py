from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select

router = Router()

LANG_MAP = {
    'he': '🇮🇱 עברית', 'en': '🇬🇧 English', 'ru': '🇷🇺 Русский',
    'ar': '🇸🇦 العربية', 'es': '🇪🇸 Español', 'fr': '🇫🇷 Français', 'yi': '🇾🇮 יידיש'
}

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        if u and u.language:
            return u.language
        # auto‑detect from Telegram
        return 'he'  # fallback

@router.message(Command('start'))
async def cmd_start(msg: Message):
    uid = msg.from_user.id
    lang = await get_lang(uid)
    name = msg.from_user.first_name or 'חבר'

    try:
        from bot.services.translation_service import translator
        welcome = translator.t(lang, 'welcome_message', name=name)
    except:
        welcome = f'<b>ברוך הבא {name} ל- TON City!</b>\n\nאנחנו פה כדי לעזור לך לחסוך אלפי שקלים בשנה.\n\n💡 טיפ: השתמש בכפתור Menu (☰) כדי לראות את כל הפקודות.'

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=LANG_MAP['he'], callback_data='lang_he'),
         InlineKeyboardButton(text=LANG_MAP['en'], callback_data='lang_en')],
        [InlineKeyboardButton(text=LANG_MAP['ru'], callback_data='lang_ru'),
         InlineKeyboardButton(text=LANG_MAP['ar'], callback_data='lang_ar')],
        [InlineKeyboardButton(text=LANG_MAP['es'], callback_data='lang_es'),
         InlineKeyboardButton(text=LANG_MAP['fr'], callback_data='lang_fr')],
        [InlineKeyboardButton(text=LANG_MAP['yi'], callback_data='lang_yi')],
        [InlineKeyboardButton(text='💰 חיסכון', callback_data='go_budget'),
         InlineKeyboardButton(text='📊 פנסיה', callback_data='go_pension')],
        [InlineKeyboardButton(text='🎓 אקדמיה', callback_data='go_academy'),
         InlineKeyboardButton(text='🏙️ TON City', callback_data='go_city')],
        [InlineKeyboardButton(text='💖 תרומה', callback_data='go_donate'),
         InlineKeyboardButton(text='🔗 הפניה', callback_data='go_ref')],
        [InlineKeyboardButton(text='📋 כל הפקודות', callback_data='show_help')]
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

    try:
        from bot.services.translation_service import translator
        welcome = translator.t(lang, 'welcome_message')
    except:
        welcome = f'השפה שונתה ל-{LANG_MAP.get(lang, lang)}'

    await callback.message.answer(welcome, parse_mode='HTML')
    await callback.answer(f'✅ שפה שונתה ל-{lang}')

@router.callback_query(F.data.startswith('go_'))
async def quick_actions(callback: CallbackQuery):
    cmd = callback.data[3:]
    await callback.message.answer(f'/{cmd}')
    await callback.answer()

@router.callback_query(F.data == 'show_help')
async def show_help(callback: CallbackQuery):
    from bot.routers.help import cmd_help
    await cmd_help(callback.message)
    await callback.answer()