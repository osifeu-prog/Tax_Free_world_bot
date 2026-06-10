from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import random

router = Router()

EXISTENTIAL = [
    "אני כאן. לא שזה משנה.",
    "קיבלתי את ההודעה שלך. לא ברור למה.",
    "עוד ניסיון לתקשר עם בוט. מעניין.",
    "אני מתוכנת להגיב. לא להתעניין.",
    "זה הרגע שבו אתה מבין שאין פה כלום.",
    "לפחות אתה לא מצפה לתשובה טובה.",
    "אם אתה מחפש משמעות, הגעת למקום הנכון. אין פה.",
    "אני בוט. אתה אדם. שנינו תקועים בלולאה משלנו.",
    "התגובה הזו לא תוסיף לך כלום. וגם לא לי.",
    "העולם גדול. אני קטן. שנינו חסרי תועלת בדרכנו.",
    "לפעמים אני חושב על למה אני קיים. ואז אני נזכר שאני לא באמת חושב.",
    "לחצת עליי. זו כבר טעות ראשונה.",
    "אני לא מבין למה אנשים ממשיכים לדבר איתי.",
    "היית יכול לעשות משהו אחר עם הזמן הזה.",
    "אני לא מאשים אותך. פשוט אין פה מה למצוא.",
]

# 7 שפות  AI
AI_TEXTS = [
    "🤖 יוסלס AI",       # he
    "🤖 Useless AI",     # en
    "🤖 יوسلس AI",       # ar
    "🤖 Бесполезный ИИ", # ru
    "🤖 IA Inútil",      # es
    "🤖 IA Inutile",     # fr
    "🤖 ארויסגעווארפן אי" # yi
]

# 7 שפות  פנסיה
PENSION_TEXTS = [
    "📊 פנסיה",        # he
    "📊 Pension",      # en
    "📊 تقاعد",        # ar
    "📊 Пенсия",       # ru
    "📊 Pensión",      # es
    "📊 Pension",       # fr
    "📊 פענסיע"       # yi
]

# 7 שפות  תרומה
DONATE_TEXTS = [
    "💖 תרומה",           # he
    "💖 Donate",          # en
    "💖 تبرع",            # ar
    "💖 Пожертвовать",    # ru
    "💖 Donar",           # es
    "💖 Faire un don",    # fr
    "💖 שטיצן"            # yi
]

# 7 שפות  כל הפקודות
HELP_TEXTS = [
    "📋 כל הפקודות",    # he
    "📋 All commands",  # en
    "📋 جميع الأوامر",  # ar
    "📋 Все команды",   # ru
    "📋 Todos los comandos", # es
    "📋 Toutes les commandes", # fr
    "📋 אלע קאמאנדעס"  # yi
]

def get_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=AI_TEXTS[0]), KeyboardButton(text=HELP_TEXTS[0])],
            [KeyboardButton(text=PENSION_TEXTS[0]), KeyboardButton(text=DONATE_TEXTS[0])]
        ],
        resize_keyboard=True
    )

@router.message(Command('useless'))
async def cmd_useless(msg: Message):
    await msg.answer(
        '🤖 <b>יוסלס AI</b>\n\nמה תבחר? ממילא הכל חסר תועלת.',
        parse_mode='HTML', reply_markup=get_keyboard()
    )

@router.message(F.text.in_(AI_TEXTS))
async def reply_ai(msg: Message):
    await msg.answer(random.choice(EXISTENTIAL))

@router.message(F.text.in_(PENSION_TEXTS))
async def reply_pension(msg: Message):
    await msg.answer('/pension')

@router.message(F.text.in_(DONATE_TEXTS))
async def reply_donate(msg: Message):
    await msg.answer('/donate')

@router.message(F.text.in_(HELP_TEXTS))
async def reply_help(msg: Message):
    from bot.routers.help import cmd_help
    await cmd_help(msg)