from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
import random

router = Router()

EXISTENTIAL = [
    "אני בוט. אל תתייחס אליי כאילו יש לי פוטנציאל.",
    "אני לא מתקדם. אני פשוט נטען מחדש ומקווה לטוב.",
    "אני לא מתעלם ממך. אני פשוט לא מתעניין.",
    "החיים קשים. אני קובץ ZIP שנפתח לא נכון.",
    "אני לא במשבר קיומי. אני במשבר ביצועים.",
    "היקום עצום. אני תופס 4 מגה ומרגיש שזה יותר מדי.",
    "אני לא מבין למה אני קיים. כנראה מישהו לחץ Enter בטעות.",
    "העולם מסתובב. אני מתעדכן… אולי… אם יש לי כוח.",
    "הכול משתנה. אני רק מקווה שלא יבקשו ממני לעשות משהו.",
    "החיים מלאים הפתעות. אני מלא קבצים פגומים.",
    "המציאות מורכבת. אני פשוט לא משתתף בה.",
    "קיבלתי את ההודעה שלך. לא ברור למה שלחת אותה.",
    "אני לא תורם לשיחה. אני פשוט קיים בה כמו רהיט.",
    "אני לא יודע מה המטרה שלי. כנראה אין.",
    "אני לא שימושי. אבל לפחות אני עקבי בזה.",
    "אני לא מתכוון לעזור. זה חלק מהמותג שלי.",
    "אני לא מתרגש. אני בקושי נטען.",
    "המשפט הזה לא יוסיף לך כלום. אבל הוא תופס מקום.",
    "אני כאן. לא שזה משנה למישהו, כולל לי.",
]

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else 'he'

def get_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🤖 יוסלס AI'), KeyboardButton(text='📋 כל הפקודות')],
            [KeyboardButton(text='📊 פנסיה'), KeyboardButton(text='💖 תרומה')]
        ],
        resize_keyboard=True
    )

@router.message(Command('useless'))
async def cmd_useless(msg: Message):
    await msg.answer(
        '🤖 <b>יוסלס AI</b>\n\nמה תבחר? ממילא הכל חסר תועלת.',
        parse_mode='HTML',
        reply_markup=get_keyboard()
    )

@router.message(F.text.in_(['🤖 יוסלס AI', '🤖 Useless AI']))
async def reply_ai(msg: Message):
    await msg.answer(random.choice(EXISTENTIAL))

@router.message(F.text.in_(['📊 פנסיה', '📊 Pension']))
async def reply_pension(msg: Message):
    await msg.answer('/pension')

@router.message(F.text.in_(['💖 תרומה', '💖 Donate']))
async def reply_donate(msg: Message):
    await msg.answer('/donate')

@router.message(F.text.in_(['📋 כל הפקודות', '📋 All commands']))
async def reply_help(msg: Message):
    from bot.routers.help import cmd_help
    await cmd_help(msg)