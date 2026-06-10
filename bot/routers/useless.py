from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select, text
from bot.database.session import engine
import random

router = Router()

USELESS_ANSWERS = {
    'he': ["🤷♂️ אין לי תשובה. גם לך אין שאלה.","🎉 מזל טוב! זכית בכלום.","📦 שום דבר לא קרה. תרגיש חופשי לשתף."],
    'en': ["🤷♂️ I have no answer. You have no question.","🎉 Congrats! You won nothing.","📦 Nothing happened. Feel free to share."],
    'ar': ["🤷♂️ ليس لدي إجابة. أنت أيضًا ليس لديك سؤال.","🎉 مبروك! لقد فزت بلا شيء.","📦 لم يحدث شيء. لا تتردد في المشاركة."],
    'ru': ["🤷♂️ У меня нет ответа. У тебя нет вопроса.","🎉 Поздравляю! Ты выиграл ничего.","📦 Ничего не произошло. Можешь поделиться."],
    'es': ["🤷♂️ No tengo respuesta. Tú no tienes pregunta.","🎉 ¡Felicidades! Ganaste nada.","📦 No pasó nada. Siéntete libre de compartir."],
    'fr': ["🤷♂️ Je n'ai pas de réponse. Tu n'as pas de question.","🎉 Félicitations ! Tu as gagné rien.","📦 Rien ne s'est passé. N'hésite pas à partager."],
    'yi': ["🤷♂️ איך האב נישט קיין ענטפער. דו האסט נישט קיין שאלה.","🎉 מזל טוב! דו האסט געווונען גארנישט.","📦 גארנישט איז געשען. פיל פר צו טיילן."]
}
ROULETTE = {
    'he': ["🎰 סובבת רולטה וזכית... בכלום!", "🎲 קובייה: 🎱. שום דבר.", "🃏 קלף: ליצן. אתה הליצן."],
    'en': ["🎰 You spun the roulette and won... nothing!", "🎲 Dice: 🎱. Nothing.", "🃏 Card: Joker. You're the joker."]
}

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else 'he'

def get_keyboard(lang):
    try:
        from bot.services.translation_service import translator
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='🤖 יוסלס AI'), KeyboardButton(text='🎲 רולטה')],
                [KeyboardButton(text='🔗 QR שלי'), KeyboardButton(text='📊 סטטיסטיקות אמת')],
                [KeyboardButton(text='💰 חיסכון'), KeyboardButton(text='📊 פנסיה')]
            ],
            resize_keyboard=True
        )
    except:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text='🤖 יוסלס AI'), KeyboardButton(text='🎲 רולטה')],
                [KeyboardButton(text='🔗 QR שלי'), KeyboardButton(text='📊 סטטיסטיקות אמת')]
            ],
            resize_keyboard=True
        )

@router.message(Command('useless'))
async def cmd_useless(msg: Message):
    lang = await get_lang(msg.from_user.id)
    kb = get_keyboard(lang)
    await msg.answer('🤖 <b>יוסלס AI</b>\n\nמה תבחר? ממילא הכל חסר תועלת.', parse_mode='HTML', reply_markup=kb)

@router.message(F.text == '🤖 יוסלס AI')
async def reply_ai(msg: Message):
    lang = await get_lang(msg.from_user.id)
    answers = USELESS_ANSWERS.get(lang, USELESS_ANSWERS['he'])
    await msg.answer(random.choice(answers))

@router.message(F.text == '🎲 רולטה')
async def reply_roulette(msg: Message):
    lang = await get_lang(msg.from_user.id)
    roulette = ROULETTE.get(lang, ROULETTE['he'])
    await msg.answer(random.choice(roulette))

@router.message(F.text == '🔗 QR שלי')
async def reply_qr(msg: Message):
    uid = msg.from_user.id
    ref_link = f"https://t.me/Tax_Free_world_bot?start=ref{uid}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={ref_link}"
    await msg.answer_photo(qr_url, caption='🔗 זה ה-QR שלך. סרוק, העתק, שתף. ממילא אין תועלת.')

@router.message(F.text == '📊 סטטיסטיקות אמת')
async def reply_stats(msg: Message):
    lang = await get_lang(msg.from_user.id)
    async with engine.begin() as conn:
        users = await conn.run_sync(lambda c: c.execute(text("SELECT COUNT(*) FROM users")).fetchone()[0])
        donations = await conn.run_sync(lambda c: c.execute(text("SELECT COUNT(*) FROM donations")).fetchone()[0])
        amount = await conn.run_sync(lambda c: c.execute(text("SELECT COALESCE(SUM(amount), 0) FROM donations")).fetchone()[0])
    ratio = round((donations / users * 100) if users else 0, 1)
    try:
        from bot.services.translation_service import translator
        header = translator.t(lang, 'stats_header')
        body = translator.t(lang, 'stats_body', users=users, donations=donations, amount=amount, ratio=ratio)
    except:
        body = f"👥 משתמשים: {users}\n💖 תרומות: {donations}\n💰 סכום: {amount} TON\n📉 יחס המרה: {ratio}%\n\n🤷♂️ אף אחד לא תורם. ואתה?"
    await msg.answer(f"{header}\n{body}", parse_mode='HTML')

@router.message(F.text == '💰 חיסכון')
async def go_budget(msg: Message):
    await msg.answer('/budget')

@router.message(F.text == '📊 פנסיה')
async def go_pension(msg: Message):
    await msg.answer('/pension')