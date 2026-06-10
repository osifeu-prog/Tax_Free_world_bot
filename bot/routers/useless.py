from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import random

router = Router()

EXISTENTIAL = {
    'he': [
        "😶🌫️ אני כאן. לא שזה משנה.",
        "📨 קיבלתי את ההודעה שלך. לא ברור למה.",
        "🤔 עוד ניסיון לתקשר עם בוט. מעניין.",
        "💤 אני מתוכנת להגיב. לא להתעניין.",
        "🕳️ זה הרגע שבו אתה מבין שאין פה כלום.",
    ],
    'en': [
        "😶🌫️ I'm here. Not that it matters.",
        "📨 Got your message. Not sure why.",
    ],
    'ru': ["😶🌫️ Я здесь. Не то чтобы это имело значение."],
    'ar': ["😶🌫️ أنا هنا. لا يهم."],
    'es': ["😶🌫️ Estoy aquí. No es que importe."],
    'fr': ["😶🌫️ Je suis là. Pas que ça importe."],
    'yi': ["😶🌫️ איך בין דא. נישט וואס עס איז וויכטיק."],
}

def get_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🔴 לחץ AI'), KeyboardButton(text='📋 כל הפקודות')],
            [KeyboardButton(text='📊 פנסיה'), KeyboardButton(text='💖 תרומה')]
        ],
        resize_keyboard=True
    )

async def get_lang(uid):
    from bot.database.session import async_session
    from bot.database.models import User
    from sqlalchemy import select
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else 'he'

@router.message(Command('useless'))
async def cmd_useless(msg: Message):
    await msg.answer('🤖 <b>היי! אני בוט מיותר.</b>\n\nאני לא בנוי לעזור, לא בנוי לתרום, רק להגיב.', parse_mode='HTML', reply_markup=get_keyboard())

# כל השפות - AI
AI_BUTTONS = [
    '🔴 לחץ AI', '🔴 Press AI', '🔴 اضغط AI', '🔴 Нажми AI',
    '🔴 Presiona AI', '🔴 Appuyez AI', '🔴 דרוק AI'
]
@router.message(F.text.in_(AI_BUTTONS))
async def reply_ai(msg: Message):
    lang = await get_lang(msg.from_user.id)
    answers = EXISTENTIAL.get(lang, EXISTENTIAL['he'])
    await msg.answer(random.choice(answers))

# כל השפות - פנסיה
PENSION_BUTTONS = [
    '📊 פנסיה', '📊 Pension', '📊 تقاعد', '📊 Пенсия',
    '📊 Pensión', '📊 Pension', '📊 פענסיע'
]
@router.message(F.text.in_(PENSION_BUTTONS))
async def reply_pension(msg: Message):
    await msg.answer('/pension')

# כל השפות - תרומה
DONATE_BUTTONS = [
    '💖 תרומה', '💖 Donate', '💖 تبرع', '💖 Пожертвовать',
    '💖 Donar', '💖 Faire un don', '💖 שטיצן'
]
@router.message(F.text.in_(DONATE_BUTTONS))
async def reply_donate(msg: Message):
    await msg.answer('/donate')

# כל השפות - עזרה
HELP_BUTTONS = [
    '📋 כל הפקודות', '📋 All commands', '📋 جميع الأوامر', '📋 Все команды',
    '📋 Todos los comandos', '📋 Toutes les commandes', '📋 אלע קאמאנדעס'
]
@router.message(F.text.in_(HELP_BUTTONS))
async def reply_help(msg: Message):
    from bot.routers.help import cmd_help
    await cmd_help(msg)