from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from bot.database.models import Course
from sqlalchemy import text
import json
from bot.config import settings

router = Router()

@router.message(Command("seed_courses"))
async def cmd_seed_courses(msg: Message):
    # בדיקת אדמין
    try:
        admin_ids = json.loads(settings.admin_ids)
    except:
        admin_ids = [int(x.strip()) for x in settings.admin_ids.split(",") if x.strip()]
    if msg.from_user.id not in admin_ids:
        await msg.answer("⛔ פקודת אדמין בלבד.")
        return

    async with async_session() as session:
        # ודא שהטבלאות קיימות
        await session.execute(text('CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(200), description TEXT, content TEXT, required_role VARCHAR(50) DEFAULT \'citizen\', order_num INTEGER DEFAULT 0, is_active BOOLEAN DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'))
        await session.execute(text('CREATE TABLE IF NOT EXISTS user_progress (id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id BIGINT, course_id INTEGER, completed_lessons TEXT DEFAULT \'[]\', score INTEGER DEFAULT 0, last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'))
        await session.commit()

        # בדוק אם כבר קיימים קורסים
        r = await session.execute(text('SELECT COUNT(*) FROM courses'))
        if r.scalar() > 0:
            await msg.answer("✅ קורסים כבר קיימים.")
            return

        courses = [
            Course(title="מבוא לקריפטו", description="למה ביטקוין ו-TON משנים את העולם", required_role="citizen", order_num=1),
            Course(title="CBDC  מטבעות בנק מרכזי", description="ההבדל בין CBDC לקריפטו חופשי", required_role="citizen", order_num=2),
            Course(title="ביזור מול ריכוז", description="איך ביזור מונע שחיתות", required_role="citizen", order_num=3),
            Course(title="NFT  זהות דיגיטלית", description="איך NFT הופך לכרטיס ביקור דיגיטלי", required_role="entrepreneur", order_num=4),
            Course(title="DAO  ארגונים מבוזרים", description="לנהל קהילה עם חוזים חכמים", required_role="leader", order_num=5),
        ]
        session.add_all(courses)
        await session.commit()
        await msg.answer(f"✅ {len(courses)} קורסים נוספו!")
