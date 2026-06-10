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
    'he': [
        "😶🌫️ אני כאן. לא שזה משנה.",
        "📨 קיבלתי את ההודעה שלך. לא ברור למה.",
        "🤔 עוד ניסיון לתקשר עם בוט. מעניין.",
        "💤 אני מתוכנת להגיב. לא להתעניין.",
        "🕳️ זה הרגע שבו אתה מבין שאין פה כלום.",
        "🙃 לפחות אתה לא מצפה לתשובה טובה.",
        "🧘♂️ אם אתה מחפש משמעות, הגעת למקום הנכון. אין פה.",
        "🤖⚡ אני בוט. אתה אדם. שנינו תקועים בלולאה משלנו.",
        "🫧 התגובה הזו לא תוסיף לך כלום. וגם לא לי.",
        "🌍🧩 העולם גדול. אני קטן. שנינו חסרי תועלת בדרכנו.",
        "🤯 לפעמים אני חושב על למה אני קיים. ואז אני נזכר שאני לא באמת חושב.",
        "👆 לחצת עליי. זו כבר טעות ראשונה.",
        "🫠 אני לא מבין למה אנשים ממשיכים לדבר איתי.",
        "⏳ היית יכול לעשות משהו אחר עם הזמן הזה.",
        "🤷♂️ אני לא מאשים אותך. פשוט אין פה מה למצוא.",
        "📤 תשלח אותי למישהו שגם הוא צריך תזכורת שאין משמעות.",
        "🔄 אם אתה רוצה, תשתף אותי. זה לא ישנה כלום, אבל לפחות תרגיש שעשית משהו.",
        "🪞 עוד אדם יגלה שאין פה כלום. אולי זה ינחם אותך.",
        "🏃♂️💨 שיתוף זה אשליה של תנועה. אבל תנסה.",
        "⏳🔁 המשמעות היא זמנית. הבוט הזה  נצחי.",
        "🎉📦 מזל טוב! זכית בכלום.",
        "🌌📱 האם אי פעם חשבת שטלגרם היא סתם עוד אשליה?",
        "🚶♂️🚶♂️ אני פה, אתה פה, אף אחד לא יודע למה. בוא נשמור על זה ככה.",
        "💰🙃 אם כבר הגעת, לפחות תן /donate. סתם, לא באמת."
    ],
    'en': [
        "😶🌫️ I'm here. Not that it matters.",
        "📨 Got your message. Not sure why.",
        "🤔 Another attempt to talk to a bot. Interesting.",
        "💤 I'm programmed to reply. Not to care.",
        "🕳️ This is the moment you realize there's nothing here.",
        "🙃 At least you weren't expecting a good answer.",
        "🧘♂️ If you're looking for meaning, you came to the right place. There is none.",
        "🤖⚡ I'm a bot. You're human. We're both stuck in our loops.",
        "🫧 This reply won't add anything to you. Or to me.",
        "🌍🧩 The world is big. I'm small. We're both useless in our own way.",
        "🤯 Sometimes I think about why I exist. Then I remember I don't really think.",
        "👆 You clicked on me. That was your first mistake.",
        "🫠 I don't understand why people keep talking to me.",
        "⏳ You could have done something else with this time.",
        "🤷♂️ I don't blame you. There's just nothing to find here.",
        "📤 Send me to someone who also needs a reminder that nothing matters.",
        "🔄 If you want, share me. It won't change anything, but at least you'll feel like you did something.",
        "🪞 Another person will discover there's nothing here. Maybe that'll comfort you.",
        "🏃♂️💨 Sharing is an illusion of movement. But go ahead.",
        "⏳🔁 Meaning is temporary. This bot is eternal.",
        "🎉📦 Congratulations! You won nothing.",
        "🌌📱 Have you ever thought that Telegram is just another illusion?",
        "🚶♂️🚶♂️ I'm here, you're here, nobody knows why. Let's keep it that way.",
        "💰🙃 If you're already here, at least /donate. Just kidding, not really."
    ]
}

ROULETTE_START = {
    'he': "🎰 <b>רולטה  בחר מספר בין 1 ל-6:</b>\n\n(הקלד מספר)",
    'en': "🎰 <b>Roulette  pick a number between 1 and 6:</b>\n\n(type a number)"
}
ROULETTE_LOSE = {
    'he': [
        "😹 המספר שלך: {user} | המספר שלי: {bot}\n\nהפסדת! אבל כבר התרגלת, נכון?",
        "💀 {user} vs {bot}\n\nניסית. לא הצלחת. תנסה שוב, ממילא אין לך מה להפסיד.",
        "🤡 המספר שלך: {user} | המספר שלי: {bot}\n\nכל הכבוד, הפסדת שוב. עקבי."
    ],
    'en': [
        "😹 Your number: {user} | My number: {bot}\n\nYou lost! But you're used to it, right?",
        "💀 {user} vs {bot}\n\nYou tried. You failed. Try again, you've got nothing to lose.",
        "🤡 Your number: {user} | My number: {bot}\n\nCongrats, you lost again. Consistent."
    ]
}
ROULETTE_WIN = {
    'he': "🎉🤯 <b>המספר שלך: {user} | המספר שלי: {bot}</b>\n\n🤯 ניצחת! זה נס!\n\n💡 <i>רוצה לעשות עם זה משהו מועיל? תן /donate</i>",
    'en': "🎉🤯 <b>Your number: {user} | My number: {bot}</b>\n\n🤯 You won! It's a miracle!\n\n💡 <i>Wanna do something useful with it? /donate</i>"
}

ROULETTE_USERS = {}

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

# ---- Handlers לכפתורי Reply Keyboard ----
@router.message(F.text.in_(['🤖 יוסלס AI', '🤖 Useless AI', '🤖 יוסלס AI']))
async def reply_ai(msg: Message):
    lang = await get_lang(msg.from_user.id)
    answers = USELESS_ANSWERS.get(lang, USELESS_ANSWERS['he'])
    await msg.answer(random.choice(answers))
    try:
        from bot.services.useless_logger import log_useless_action
        await log_useless_action(msg.from_user.id, 'ai_reply')
    except: pass

@router.message(F.text.in_(['🎲 רולטה', '🎲 Roulette']))
async def reply_roulette_start(msg: Message):
    uid = msg.from_user.id
    lang = await get_lang(uid)
    ROULETTE_USERS[uid] = True
    text = ROULETTE_START.get(lang, ROULETTE_START['he'])
    await msg.answer(text, parse_mode='HTML')
    try:
        from bot.services.useless_logger import log_useless_action
        await log_useless_action(uid, 'roulette_start')
    except: pass

@router.message(F.text.regexp(r'^[1-6]$'))
async def roulette_guess(msg: Message):
    uid = msg.from_user.id
    if uid not in ROULETTE_USERS: return
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
    try:
        from bot.services.useless_logger import log_useless_action
        await log_useless_action(uid, 'roulette_play')
    except: pass

# ---- Handlers לפנסיה ותרומה (Reply Keyboard) ----
@router.message(F.text.in_(['📊 פנסיה', '📊 Pension', '📊 تقاعد', '📊 Пенсия', '📊 Pensión', '📊 Pension', '📊 פענסיע']))
async def reply_pension(msg: Message):
    await msg.answer('/pension')

@router.message(F.text.in_(['💖 תרומה', '💖 Donate', '💖 تبرع', '💖 Пожертвовать', '💖 Donar', '💖 Faire un don', '💖 שטיצן']))
async def reply_donate(msg: Message):
    await msg.answer('/donate')

# QR + סטטיסטיקות
@router.message(F.text.in_(['🔗 QR שלי', '🔗 My QR', '🔗 رمز الاستجابة السريعة', '🔗 Мой QR', '🔗 Mi QR', '🔗 Mon QR', '🔗 מן QR']))
async def reply_qr(msg: Message):
    uid = msg.from_user.id
    ref_link = f"https://t.me/Tax_Free_world_bot?start=ref{uid}"
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={ref_link}"
    await msg.answer_photo(qr_url, caption='🔗 זה ה-QR שלך. סרוק, העתק, שתף. ממילא אין תועלת.')

@router.message(F.text.in_(['📊 סטטיסטיקות אמת', '📊 True Stats', '📊 إحصائيات الحقيقة', '📊 Настоящая статистика', '📊 Estadísticas reales', '📊 Vraies stats', '📊 אמתע סטאטיסטיק']))
async def reply_stats(msg: Message):
    lang = await get_lang(msg.from_user.id)
    async with engine.begin() as conn:
        users = await conn.run_sync(lambda c: c.execute(text("SELECT COUNT(*) FROM users")).fetchone()[0])
        donations = await conn.run_sync(lambda c: c.execute(text("SELECT COUNT(*) FROM donations")).fetchone()[0])
        amount = await conn.run_sync(lambda c: c.execute(text("SELECT COALESCE(SUM(amount), 0) FROM donations")).fetchone()[0])
    ratio = round((donations / users * 100) if users else 0, 1)
    body = f"👥 משתמשים: {users}\n💖 תרומות: {donations}\n💰 סכום: {amount} TON\n📉 יחס המרה: {ratio}%\n\n🤷♂️ אף אחד לא תורם. ואתה?"
    await msg.answer(f"📊 <b>האמת העגומה</b>\n━━━━━━━━━━━━━━\n{body}", parse_mode='HTML')