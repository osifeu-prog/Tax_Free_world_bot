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
    lang = await get_lang(msg.from_user.id)
    name = msg.from_user.first_name or "חבר"
    text = translator.t(lang, "welcome_message", name=name)
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 מחשבון ויזואלי", callback_data="open_miniapp")],
        [InlineKeyboardButton(text="💰 חיסכון", callback_data="go_budget"),
         InlineKeyboardButton(text="📊 פנסיה", callback_data="go_pension")],
        [InlineKeyboardButton(text="🎓 אקדמיה", callback_data="go_academy"),
         InlineKeyboardButton(text="🏙️ TON City", callback_data="go_city")],
        [InlineKeyboardButton(text="🔗 הפניה", callback_data="go_ref"),
         InlineKeyboardButton(text="💖 תרומה", callback_data="go_donate")]
    ])
    await msg.answer(text, parse_mode="HTML", reply_markup=kb)

@router.callback_query(F.data == "open_miniapp")
async def open_miniapp(callback: CallbackQuery):
    await callback.answer("📱 פותח מחשבון...")

@router.callback_query(F.data.startswith("go_"))
async def quick_menu(callback: CallbackQuery):
    await callback.answer("🔄 מעביר...")
    # כאן אפשר להוסיף קריאה לפקודות אחרות
