from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

router = Router()

@router.message(Command("app"))
async def open_webapp(msg: Message):
    web_app_url = "https://taxfreeworldbot-production.up.railway.app/public/index.html"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 פתח את Tax Free World", web_app=WebAppInfo(url=web_app_url))]
    ])
    await msg.answer("📱 <b>הדשבורד הדיגיטלי שלך</b>\n\nלחץ לפתיחה:", reply_markup=kb, parse_mode="HTML")
