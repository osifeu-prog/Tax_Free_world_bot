from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text

router = Router()

@router.message(Command("report"))
async def cmd_report(msg: Message):
    async with engine.connect() as conn:
        users = await conn.scalar(text("SELECT count(*) FROM users"))
        he_users = await conn.scalar(text("SELECT count(*) FROM users WHERE language='he'"))
        en_users = await conn.scalar(text("SELECT count(*) FROM users WHERE language='en'"))
        ar_users = await conn.scalar(text("SELECT count(*) FROM users WHERE language='ar'"))
        try:
            referrals = await conn.scalar(text("SELECT count(*) FROM users WHERE referred_by IS NOT NULL"))
        except:
            referrals = 0
    await msg.answer(
        f"📊 <b>דוח מערכת</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"👥 סהכ משתמשים: {users}\n"
        f"🇮🇱 עברית: {he_users}\n"
        f"🇬🇧 English: {en_users}\n"
        f"🇸🇦 العربية: {ar_users}\n"
        f"🔗 הפניות: {referrals}",
        parse_mode="HTML"
    )
