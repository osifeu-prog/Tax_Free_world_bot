from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
import random

router = Router()

USELESS_ANSWERS = {
    'he': [
        "למה שתצפה למשהו? 🤷♂️",
        "אין לי תשובה. גם לך אין שאלה אמיתית.",
        "שלחת הודעה לבוט שלא עושה כלום. מרגיש טוב?",
        "גם אני מתוכנת לא לעשות כלום. ואתה?",
        "תשתף אותי עם חבר. אולי הוא יצחק. אתה תמשיך להרגיש כלום.",
        "המשמעות היא זמנית. הבוט הזה  נצחי.",
        "מזל טוב! זכית בכלום. 🎉",
        "האם אי פעם חשבת שטלגרם היא סתם עוד אשליה?",
        "אני פה, אתה פה, אף אחד לא יודע למה. בוא נשמור על זה ככה.",
        "אם כבר הגעת, לפחות תן /donate. סתם, לא באמת."
    ],
    'en': [
        "Why would you expect anything? 🤷♂️",
        "I have no answer. You have no real question.",
        "You messaged a bot that does nothing. Feeling good?",
        "I'm programmed to do nothing. You?",
        "Share me with a friend. Maybe they'll laugh. You'll still feel nothing.",
        "Meaning is temporary. This bot is eternal.",
        "Congratulations! You won nothing. 🎉",
        "Have you ever thought that Telegram is just another illusion?",
        "I'm here, you're here, nobody knows why. Let's keep it that way.",
        "If you're already here, at least /donate. Just kidding, not really."
    ],
    'ar': [
        "لماذا تتوقع أي شيء؟ 🤷♂️",
        "ليس لدي إجابة. أنت أيضًا ليس لديك سؤال حقيقي.",
        "لقد أرسلت رسالة إلى بوت لا يفعل شيئًا. هل تشعر بتحسن؟",
        "أنا مبرمج على ألا أفعل شيئًا. وأنت؟",
        "شاركني مع صديق. ربما يضحك. أنت ستستمر في الشعور بلا شيء.",
        "المعنى مؤقت. هذا البوت أبدي.",
        "مبروك! لقد فزت بلا شيء. 🎉",
        "هل فكرت يومًا أن تيليجرام هو مجرد وهم آخر؟",
        "أنا هنا، وأنت هنا، لا أحد يعرف لماذا. دعنا نبقيها هكذا.",
        "إذا كنت هنا بالفعل، على الأقل /donate. فقط أمزح، ليس حقًا."
    ],
    'ru': [
        "Зачем ты чего-то ждёшь? 🤷♂️",
        "У меня нет ответа. У тебя нет настоящего вопроса.",
        "Ты написал боту, который ничего не делает. Тебе хорошо?",
        "Я запрограммирован ничего не делать. А ты?",
        "Поделись мной с другом. Может, он посмеётся. Ты всё равно ничего не почувствуешь.",
        "Смысл временен. Этот бот вечен.",
        "Поздравляю! Ты выиграл ничего. 🎉",
        "Ты когда-нибудь думал, что Телеграм — это просто ещё одна иллюзия?",
        "Я здесь, ты здесь, никто не знает зачем. Давай так и оставим.",
        "Если ты уже здесь, хотя бы /donate. Шучу, не совсем."
    ],
    'es': [
        "¿Por qué esperarías algo? 🤷♂️",
        "No tengo respuesta. Tú no tienes una pregunta real.",
        "Enviaste un mensaje a un bot que no hace nada. ¿Te sientes bien?",
        "Estoy programado para no hacer nada. ¿Tú?",
        "Compárteme con un amigo. Quizás se ría. Tú seguirás sintiendo nada.",
        "El significado es temporal. Este bot es eterno.",
        "¡Felicidades! Ganaste nada. 🎉",
        "¿Alguna vez pensaste que Telegram es solo otra ilusión?",
        "Estoy aquí, tú estás aquí, nadie sabe por qué. Dejémoslo así.",
        "Si ya estás aquí, al menos /donate. Es broma, no realmente."
    ],
    'fr': [
        "Pourquoi t'attendrais-tu à quelque chose ? 🤷♂️",
        "Je n'ai pas de réponse. Tu n'as pas de vraie question.",
        "Tu as envoyé un message à un bot qui ne fait rien. Tu te sens bien ?",
        "Je suis programmé pour ne rien faire. Et toi ?",
        "Partage-moi avec un ami. Peut-être qu'il rira. Tu continueras à ne rien ressentir.",
        "Le sens est temporaire. Ce bot est éternel.",
        "Félicitations ! Tu as gagné rien. 🎉",
        "As-tu déjà pensé que Telegram n'est qu'une autre illusion ?",
        "Je suis là, tu es là, personne ne sait pourquoi. Gardons-le comme ça.",
        "Si tu es déjà là, au moins /donate. Je plaisante, pas vraiment."
    ],
    'yi': [
        "פארוואס וואלטסטו ערווארטן עפעס? 🤷♂️",
        "איך האב נישט קיין ענטפער. דו האסט נישט קיין אמתע שאלה.",
        "דו האסט געשריבן צו א באט וואס טוט גארנישט. פילסטו זיך גוט?",
        "איך בין פראגראמירט צו טאן גארנישט. און דו?",
        "טייל מיך מיט א פרנד. אפשר ער וועט לאכן. דו וועסט ווטער פילן גארנישט.",
        "דער זין איז צטווליק. דער באט איז אייביק.",
        "מזל טוב! דו האסט געווונען גארנישט. 🎉",
        "צי האסטו אמאל געטראכט אז טעלעגראם איז נאר נאך אן אילוזיע?",
        "איך בין דא, דו ביסט דא, קיינער ווייסט נישט פארוואס. לאמיר עס האלטן אזוי.",
        "אויב דו ביסט שוין דא, לפחות /donate. איך שפאס, נישט טאקע."
    ]
}

async def get_lang(uid):
    async with async_session() as s:
        u = (await s.execute(select(User).where(User.telegram_id == uid))).scalar_one_or_none()
        return u.language if u and u.language else 'he'

@router.message(Command('useless'))
async def cmd_useless(msg: Message):
    lang = await get_lang(msg.from_user.id)
    try:
        from bot.services.translation_service import translator
        title = translator.t(lang, 'useless_title')
        prompt = translator.t(lang, 'useless_prompt')
        btn = translator.t(lang, 'useless_button')
    except:
        title = '🤖 יוסלס AI'
        prompt = 'תגיד לי משהו חסר תועלת:'
        btn = '🎲 תן לי תשובה עקומה'
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn, callback_data='useless_answer')],
        [InlineKeyboardButton(text='🔗 שתף את היוסלס', switch_inline_query='גם אתה חייב לנסות את @Tax_Free_world_bot  פקודת /useless!')]
    ])
    await msg.answer(f'<b>{title}</b>\n\n{prompt}', parse_mode='HTML', reply_markup=kb)

@router.callback_query(F.data == 'useless_answer')
async def useless_answer(callback: CallbackQuery):
    lang = await get_lang(callback.from_user.id)
    answers = USELESS_ANSWERS.get(lang, USELESS_ANSWERS['he'])
    answer = random.choice(answers)
    await callback.message.answer(f'🤖 {answer}')
    await callback.answer()