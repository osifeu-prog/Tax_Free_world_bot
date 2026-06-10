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
    'en': ["🤷♂️ I have no answer. You have no question.","🎉 Congrats! You won nothing.","📦 Nothing happened. Feel free to share."]
}

ROULETTE_START = {
    'he': "🎰 <b>רולטה  בחר מספר בין 1 ל-6:</b>\n\n(הקלד מספר)",
    'en': "🎰 <b>Roulette  pick a number between 1 and 6:</b>\n\n(type a number)"
}
ROULETTE_LOSE = {
    'he': ["😹 המספר שלך: {user} | המספר שלי: {bot}\n\nהפסדת! אבל כבר התרגלת, נכון?",
           "💀 {user} vs {bot}\n\nניסית. לא הצלחת. תנסה שוב, ממילא אין לך מה להפסיד.",
           "🤡 המספר שלך: {user} | המספר שלי: {bot}\n\nכל הכבוד, הפסדת שוב. עקבי."],
    'en': ["😹 Your number: {user} | My number: {bot}\n\nYou lost! But you're used to it, right?",
           "💀 {user} vs {bot}\n\nYou tried. You failed. Try again, you've got nothing to lose.",
           "🤡 Your number: {user} | My number: {bot}\n\nCongrats, you lost again. Consistent."]
}
ROULETTE_WIN = {
    'he': "🎉 <b>המספר שלך: {user} | המספר שלי: {bot}</b>\n\n🤯 ניצחת! זה נס!\n\n💡 <i>רוצה לעשות עם זה משהו מועיל? תן /donate</i>",
    'en': "🎉 <b>Your number: {user} | My number: {bot}</b>\n\n🤯 You won! It's a miracle!\n\n💡 <i>Wanna do something useful with it? /donate</i>"
}

ROULETTE_USERS = {}

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else 'he'

def get_keyboard(lang):
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
async def reply_roulette_start(msg: Message):
    uid = msg.from_user.id
    lang = await get_lang(uid)
    ROULETTE_USERS[uid] = True
    text = ROULETTE_START.get(lang, ROULETTE_START['he'])
    await msg.answer(text, parse_mode='HTML')

@router.message(F.text.regexp(r'^[1-6]$'))
async def roulette_guess(msg: Message):
    uid = msg.from_user.id
    if uid not in ROULETTE_USERS:
        return
    del ROULETTE_USERS[uid]
    lang = await get_lang(uid)
    user_num = int(msg.text)
    bot_num = random.randint(1, 6)
    if user_num == bot_num:
        text = ROULETTE_WIN.get(lang, ROULETTE_WIN['he']).format(user=user_num, bot=bot_num)
    else:
        texts = ROULETTE_LOSE.get(lang, ROULETTE_LOSE['he'])
        text = random.choice(texts).format(user=user_num, bot=bot_num)
    await msg.answer(text, parse_mode='HTML')

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
    body = f"👥 משתמשים: {users}\n💖 תרומות: {donations}\n💰 סכום: {amount} TON\n📉 יחס המרה: {ratio}%\n\n🤷♂️ אף אחד לא תורם. ואתה?"
    await msg.answer(f"📊 <b>האמת העגומה</b>\n━━━━━━━━━━━━━━\n{body}", parse_mode='HTML')