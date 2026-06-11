from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from sqlalchemy import text
from bot.utils.i18n import i18n

router = Router()

def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇮🇱 עברית", callback_data="set_lang_he")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en")],
    ])

@router.message(Command("language"))
@router.message(Command("lang"))
async def cmd_language(msg: Message):
    await msg.answer(
        "🌍 <b>בחר שפה / Choose language</b>",
        parse_mode="HTML",
        reply_markup=get_language_keyboard()
    )

@router.callback_query(F.data.startswith("set_lang_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[2]
    uid = callback.from_user.id
    
    async with async_session() as s:
        await s.execute(
            text("UPDATE user_preferences SET language = :lang WHERE user_id = :uid"),
            {"lang": lang, "uid": uid}
        )
        await s.commit()
    
    text = "✅ השפה שונתה לעברית!" if lang == "he" else "✅ Language changed to English!"
    await callback.message.edit_text(text)
    await callback.answer()
