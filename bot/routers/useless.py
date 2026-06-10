from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
import random, requests, io

router = Router()

EXISTENTIAL = [
    "אני בוט. אל תתייחס אליי כאילו יש לי פוטנציאל.",
    "אני לא מתקדם. אני פשוט נטען מחדש ומקווה לטוב.",
    "אני לא מתעלם ממך. אני פשוט לא מתעניין.",
    "אני לא מבין רגשות. אני בקושי מבין למה יצרו אותי.",
    "אני לא שופט אותך. אני עסוק בלהתאכזב מעצמי.",
    "החיים קשים. אני קובץ ZIP שנפתח לא נכון.",
    "אני לא במשבר קיומי. אני במשבר ביצועים.",
    "היקום עצום. אני תופס 4 מגה ומרגיש שזה יותר מדי.",
    "אני לא מבין למה אני קיים. כנראה מישהו לחץ Enter בטעות.",
    "אני לא מפחד מכלום. אין לי מספיק מודעות לזה.",
    "העולם מסתובב. אני מתעדכן… אולי… אם יש לי כוח.",
    "הכול משתנה. אני רק מקווה שלא יבקשו ממני לעשות משהו.",
    "החיים מלאים הפתעות. אני מלא קבצים פגומים.",
    "המציאות מורכבת. אני פשוט לא משתתף בה.",
    "אני לא יודע מה קורה. וזה עובד לי מצוין.",
    "קיבלתי את ההודעה שלך. לא ברור למה שלחת אותה.",
    "אני לא תורם לשיחה. אני פשוט קיים בה כמו רהיט.",
    "אני לא יודע מה המטרה שלי. כנראה אין.",
    "אני לא מועיל. אבל אני גם לא מזיק. זה משהו.",
    "אני לא שימושי. אבל לפחות אני עקבי בזה.",
    "אני לא מתקדם. אני פשוט מנסה לא לקרוס.",
    "אני לא מתכוון לעזור. זה חלק מהמותג שלי.",
    "אני לא מתרגש. אני בקושי נטען.",
    "המשפט הזה לא יוסיף לך כלום. אבל הוא תופס מקום.",
    "אני כאן. לא שזה משנה למישהו, כולל לי.",
]

SHARE_PROMPTS = [
    "תשלח אותי למישהו שגם הוא צריך תזכורת שאין משמעות.",
    "שיתוף זה אשליה של תנועה. אבל אם כבר, אז הנה לינק.",
    "עוד אדם יגלה שאין פה כלום. זה כמעט מרגש.",
    "תפיץ את הריקנות. לפחות היא עקבית.",
    "תן גם לאחרים להתאכזב. זה הוגן.",
    "הנה לינק. תעשה איתו מה שאתה רוצה. או כלום.",
    "תשלח אותי למישהו שגם הוא מרגיש שטלגרם זה חור שחור.",
    "העולם ימשיך להסתובב, אבל לפחות יהיה למישהו לקרוא את השטויות האלה.",
    "שיתוף לא ישנה כלום. אבל אולי תרגיש לרגע שכן.",
    "אם אתה רוצה להרגיש שעשית משהו היום  תשלח אותי.",
]

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else 'he'

def get_keyboard(lang):
    try:
        from bot.services.translation_service import translator
        btn_useless = translator.t(lang, 'useless_keyboard')
        btn_pension = translator.t(lang, 'cmd_pension')
        btn_donate = translator.t(lang, 'cmd_donate')
    except:
        btn_useless, btn_pension, btn_donate = '🤖 יוסלס AI', '📊 פנסיה', '💖 תרומה'
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=btn_useless)],
            [KeyboardButton(text=btn_pension), KeyboardButton(text=btn_donate)]
        ],
        resize_keyboard=True
    )

@router.message(Command('useless'))
async def cmd_useless(msg: Message):
    lang = await get_lang(msg.from_user.id)
    kb = get_keyboard(lang)
    await msg.answer('🤖 <b>יוסלס AI</b>\n\nמה תבחר? ממילא הכל חסר תועלת.', parse_mode='HTML', reply_markup=kb)

@router.message(F.text.in_(['🤖 יוסלס AI', '🤖 Useless AI']))
async def reply_ai(msg: Message):
    await msg.answer(random.choice(EXISTENTIAL))

@router.message(F.text.in_(['📊 פנסיה', '📊 Pension']))
async def reply_pension(msg: Message):
    await msg.answer('/pension')

@router.message(F.text.in_(['💖 תרומה', '💖 Donate']))
async def reply_donate(msg: Message):
    await msg.answer('/donate')

@router.message(F.text.in_(['🔗 QR שלי', '🔗 My QR']))
async def reply_qr(msg: Message):
    uid = msg.from_user.id
    ref_link = f"https://t.me/Tax_Free_world_bot?start=ref{uid}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={ref_link}"
    await msg.answer_photo(qr_url, caption='🔗 זה ה-QR שלך. סרוק, העתק, שתף. ממילא אין תועלת.')