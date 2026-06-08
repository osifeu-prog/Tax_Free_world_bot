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
        # events log stats
        pension_starts = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='pension_start'")) or 0
        pension_finish = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='pension_finish'")) or 0
        households_created = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='household_create'")) or 0
        course_starts = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='course_start'")) or 0
        course_completions = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='course_finish'")) or 0
        donate_views = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='donate_view'")) or 0
        qr_generated = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='qr_view'")) or 0
    await msg.answer(
        f"📊 <b>דוח מערכת  OMNI Control Plane</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👥 סהכ משתמשים: {users}\n"
        f"🇮🇱 עברית: {he_users}  🇬🇧 English: {en_users}  🇸🇦 العربية: {ar_users}\n\n"
        f"💼 פנסיה:\n"
        f"  - חישובים שהחלו: {pension_starts}\n"
        f"  - חישובים שהסתיימו: {pension_finish}\n\n"
        f"🏠 משקי בית:\n"
        f"  - נוצרו: {households_created}\n\n"
        f"📚 אקדמיה:\n"
        f"  - התחילו קורס: {course_starts}\n"
        f"  - סיימו קורס: {course_completions}\n\n"
        f"💖 תרומות:\n"
        f"  - צפיות במסך תרומה: {donate_views}\n\n"
        f"🔗 Referral:\n"
        f"  - QR שנוצרו: {qr_generated}\n",
        parse_mode="HTML"
    )
