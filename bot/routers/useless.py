from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
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
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🤖 יוסלס AI'), KeyboardButton(text='🎲 רולטה')],
            [KeyboardButton(text='🔗 QR שלי'), KeyboardButton(text='📤 שתף')]
        ],
        resize_keyboard=True
    )

@router.message(Command('useless'))
async def cmd_useless(msg: Message):
    lang = await get_lang(msg.from_user.id)
    kb = get_keyboard(lang)
    await msg.answer('🤖 <b>יוסלס AI</b>\n\nלחץ על אחד הכפתורים:', parse_mode='HTML', reply_markup=kb)

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

@router.message(F.text == '📤 שתף')
async def reply_share(msg: Message):
    await msg.answer(
        f'📤 <b>שתף את היוסלס!</b>\n\nהשתמש בקישור:\nhttps://t.me/Tax_Free_world_bot?start=ref{msg.from_user.id}',
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔗 שתף עם חברים', switch_inline_query='גם אתה חייב לנסות את @Tax_Free_world_bot  פקודת /useless!')]
        ])
    )