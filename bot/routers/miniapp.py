from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

router = Router()

@router.message(Command("miniapp"))
async def cmd_miniapp(msg: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 פתח מחשבון ויזואלי", web_app=WebAppInfo(url="https://your-domain.com/landing/miniapp.html"))]
    ])
    await msg.answer("לחץ כדי לפתוח את המחשבון בתוך טלגרם:", reply_markup=kb)
