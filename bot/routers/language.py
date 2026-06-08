from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from bot.services.translation_service import translator
from sqlalchemy import select

router = Router()

LANGS = {
    "he": "🇮🇱 עברית",
    "en": "🇺🇸 English",
    "ru": "🇷🇺 Русский"
}

@router.message(Command("language"))
async def cmd_language(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=name, callback_data=f"setlang_{code}")]
        for code, name in LANGS.items()
    ])
    await msg.answer(translator.t("he", "choose_language"), reply_markup=kb)

@router.callback_query(F.data.startswith("setlang_"))
async def on_set_lang(call: CallbackQuery):
    lang = call.data.split("_")[1]
    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == call.from_user.id)
        user = (await session.execute(stmt)).scalar_one_or_none()
        if user:
            user.language = lang
        else:
            user = User(telegram_id=call.from_user.id, language=lang)
            session.add(user)
        await session.commit()
    text = translator.t(lang, "language_saved", language=LANGS[lang])
    await call.message.edit_text(text)
    await call.answer()
