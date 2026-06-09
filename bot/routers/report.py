from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import engine
from sqlalchemy import text

router = Router()

@router.message(Command("report"))
async def cmd_report(msg: Message):
    async with engine.connect() as conn:
        total = await conn.scalar(text("SELECT count(*) FROM users")) or 0
        he = await conn.scalar(text("SELECT count(*) FROM users WHERE language='he'")) or 0
        en = await conn.scalar(text("SELECT count(*) FROM users WHERE language='en'")) or 0
        ru = await conn.scalar(text("SELECT count(*) FROM users WHERE language='ru'")) or 0
        es = await conn.scalar(text("SELECT count(*) FROM users WHERE language='es'")) or 0
        fr = await conn.scalar(text("SELECT count(*) FROM users WHERE language='fr'")) or 0
        ar = await conn.scalar(text("SELECT count(*) FROM users WHERE language='ar'")) or 0

        he_pct = (he / total * 100) if total else 0
        en_pct = (en / total * 100) if total else 0
        ru_pct = (ru / total * 100) if total else 0
        es_pct = (es / total * 100) if total else 0
        fr_pct = (fr / total * 100) if total else 0
        ar_pct = (ar / total * 100) if total else 0

        # events_log stats
        pension_starts = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='pension_start'")) or 0
        pension_finish = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='pension_finish'")) or 0
        households_created = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='household_create'")) or 0
        course_starts = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='course_start'")) or 0
        course_finish = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='course_finish'")) or 0
        donate_views = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='donate_view'")) or 0
        qr_generated = await conn.scalar(text("SELECT count(*) FROM events_log WHERE event_type='qr_view'")) or 0

    await msg.answer(
        f"📊 <b>דוח מערכת  OMNI Control Plane</b>\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👥 סהכ משתמשים: {total}\n"
        f"🌐 <b>שפות:</b>\n"
        f"  🇮🇱 עברית: {he} ({he_pct:.0f}%)\n"
        f"  🇬🇧 English: {en} ({en_pct:.0f}%)\n"
        f"  🇷🇺 Русский: {ru} ({ru_pct:.0f}%)\n"
        f"  🇪🇸 Español: {es} ({es_pct:.0f}%)\n"
        f"  🇫🇷 Français: {fr} ({fr_pct:.0f}%)\n"
        f"  🇸🇦 العربية: {ar} ({ar_pct:.0f}%)\n\n"
        f"💼 פנסיה:\n"
        f"  - חישובים שהחלו: {pension_starts}\n"
        f"  - חישובים שהסתיימו: {pension_finish}\n\n"
        f"🏠 משקי בית:\n"
        f"  - נוצרו: {households_created}\n\n"
        f"📚 אקדמיה:\n"
        f"  - התחילו קורס: {course_starts}\n"
        f"  - סיימו קורס: {course_finish}\n\n"
        f"💖 תרומות:\n"
        f"  - צפיות במסך תרומה: {donate_views}\n\n"
        f"🔗 Referral:\n"
        f"  - QR שנוצרו: {qr_generated}",
        parse_mode="HTML"
    )
