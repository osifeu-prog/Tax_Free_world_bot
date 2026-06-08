from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.services.translation_service import translator

router = Router()

@router.message(Command("translations"))
async def cmd_translations(msg: Message):
    missing = {}
    for lang in ["he", "en", "ar", "ru"]:
        loc = translator.locales.get(lang, {})
        missing[lang] = [k for k in translator.locales["he"] if k not in loc]
    text = "📊 <b>סטטוס תרגומים</b>\n"
    for lang, keys in missing.items():
        text += f"{lang}: {len(keys)} חסרים\n"
    await msg.answer(text, parse_mode="HTML")
