from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.session import async_session
from bot.database.models import User
from sqlalchemy import select
from bot.services.translation_service import translator

router = Router()

async def get_lang(user_id: int) -> str:
    async with async_session() as s:
        user = (await s.execute(select(User).where(User.telegram_id == user_id))).scalar_one_or_none()
        return user.language if user and user.language else "he"

@router.message(Command("start"))
async def cmd_start(msg: Message):
    user_id = msg.from_user.id
    lang = await get_lang(user_id)
    
    welcome_text = translator.t(lang, "welcome_message", name=msg.from_user.first_name or "חבר")
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 מחשבון ויזואלי", callback_data="open_miniapp")],
        [InlineKeyboardButton(text="💰 חיסכון & תקציב", callback_data="go_budget"),
         InlineKeyboardButton(text="📊 פנסיה", callback_data="go_pension")],
        [InlineKeyboardButton(text="🎓 אקדמיה", callback_data="go_academy"),
         InlineKeyboardButton(text="🏙️ TON City", callback_data="go_city")],
        [InlineKeyboardButton(text="🔗 הפניה + בונוס", callback_data="go_ref"),
         InlineKeyboardButton(text="💖 תרומה", callback_data="go_donate")],
        [InlineKeyboardButton(text="🌐 שנה שפה", callback_data="change_lang")]
    ])
    
    await msg.answer(welcome_text, parse_mode="HTML", reply_markup=kb)

@router.callback_query(F.data == "open_miniapp")
async def open_miniapp(callback: CallbackQuery):
    await callback.answer("📱 פותח מחשבון ויזואלי...")

@router.callback_query(F.data.startswith("go_"))
async def handle_quick_menu(callback: CallbackQuery):
    action = callback.data[3:]
    lang = await get_lang(callback.from_user.id)
    handlers = {
        "budget": ("bot.routers.budget", "cmd_budget"),
        "pension": ("bot.routers.pension", "cmd_pension"),
        "academy": ("bot.routers.academy", "cmd_academy"),
        "city": ("bot.routers.city", "cmd_city"),
        "ref": ("bot.routers.ref", "cmd_ref"),
        "donate": ("bot.routers.donate", "cmd_donate")
    }
    if action in handlers:
        try:
            module_name, func_name = handlers[action]
            module = __import__(module_name, fromlist=[func_name])
            func = getattr(module, func_name)
            await func(callback.message)
        except:
            await callback.message.answer("⚠️ הפיצ'ר זמנית לא זמין")
    await callback.answer()

@router.callback_query(F.data == "change_lang")
async def change_lang(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇮🇱 עברית", callback_data="lang_he"),
         InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
         InlineKeyboardButton(text="🇪🇸 Español", callback_data="lang_es")],
        [InlineKeyboardButton(text="🇫🇷 Français", callback_data="lang_fr")]
    ])
    await callback.message.edit_text("🌍 בחר שפה:", reply_markup=kb)
    await callback.answer()
