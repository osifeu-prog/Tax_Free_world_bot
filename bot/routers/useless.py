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
        "🙃 לפחות אתה לא מצפה לתשובה טובה.",
        "🧘♂️ אם אתה מחפש משמעות, הגעת למקום הנכון. אין פה.",
        "🤖⚡ אני בוט. אתה אדם. שנינו תקועים בלולאה.",
        "🫧 התגובה הזו לא תוסיף לך כלום. וגם לא לי.",
        "🌍🧩 העולם גדול. אני קטן. שנינו חסרי תועלת.",
    ],
    'en': [
        "😶🌫️ I'm here. Not that it matters.",
        "📨 Got your message. Not sure why.",
        "🤔 Another attempt to talk to a bot. Interesting.",
        "💤 I'm programmed to reply. Not to care.",
        "🕳️ This is the moment you realize there's nothing here.",
        "🙃 At least you weren't expecting a good answer.",
    ],
    'ru': [
        "😶🌫️ Я здесь. Не то чтобы это имело значение.",
        "📨 Получил твоё сообщение. Непонятно зачем.",
    ],
    'ar': [
        "😶🌫️ أنا هنا. لا يهم.",
        "📨 وصلتني رسالتك. لا أعرف لماذا.",
    ],
    'es': [
        "😶🌫️ Estoy aquí. No es que importe.",
        "📨 Recibí tu mensaje. No sé por qué.",
    ],
    'fr': [
        "😶🌫️ Je suis là. Pas que ça importe.",
        "📨 J'ai reçu ton message. Je ne sais pas pourquoi.",
    ],
    'yi': [
        "😶🌫️ איך בין דא. נישט וואס עס איז וויכטיק.",
        "📨 איך האב באקומען דן אנזאג. נישט וויסן פארוואס.",
    ],
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

@router.message(F.text.in_(['🔴 לחץ AI', '🔴 Press AI', '🔴 اضغط AI', '🔴 Нажми AI', '🔴 Presiona AI', '🔴 Appuyez AI', '🔴 דרוק AI']))
async def reply_ai(msg: Message):
    lang = await get_lang(msg.from_user.id)
    answers = EXISTENTIAL.get(lang, EXISTENTIAL['he'])
    await msg.answer(random.choice(answers))