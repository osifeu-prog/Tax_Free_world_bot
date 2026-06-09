from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
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
    lang = await get_lang(msg.from_user.id)
    name = msg.from_user.first_name or "חבר"
    
    text = translator.t(lang, "welcome_message", name=name)
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 מחשבון ויזואלי", callback_data="open_miniapp")],
        [InlineKeyboardButton(text="💰 חיסכון", callback_data="menu_budget"),
         InlineKeyboardButton(text="📊 פנסיה", callback_data="menu_pension")],
        [InlineKeyboardButton(text="🎓 אקדמיה", callback_data="menu_academy"),
         InlineKeyboardButton(text="🏙️ TON City", callback_data="menu_city")],
        [InlineKeyboardButton(text="🔗 הפניה", callback_data="menu_ref"),
         InlineKeyboardButton(text="💖 תרומה", callback_data="menu_donate")],
        [InlineKeyboardButton(text="📋 תפריט מלא", callback_data="show_menu")]
    ])
    
    await msg.answer(text, parse_mode="HTML", reply_markup=kb)

@router.callback_query(F.data.startswith("menu_"))
async def handle_menu(callback: CallbackQuery):
    action = callback.data[5:]
    await callback.answer("🔄 מעביר...")
    if action == "budget":
        await callback.message.answer("💰 /budget - מחשבון תקציב")
    elif action == "pension":
        await callback.message.answer("📊 /pension - מחשבון פנסיה")
    elif action == "academy":
        await callback.message.answer("🎓 /academy - אקדמיה")
    elif action == "city":
        await callback.message.answer("🏙️ /city - TON City")
    elif action == "ref":
        await callback.message.answer("🔗 /ref - הפניה")
    elif action == "donate":
        await callback.message.answer("💖 /donate - תרומה")
    elif action == "show_menu":
        from bot.routers.menu import cmd_menu
        await cmd_menu(callback.message)
