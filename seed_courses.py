import asyncio
from bot.database.session import async_session
from bot.database.models import Course
from sqlalchemy.ext.asyncio import AsyncSession

async def seed_courses():
    async with async_session() as session:
        # בדיקה אם כבר קיימים
        existing = (await session.execute("SELECT COUNT(*) FROM courses")).scalar()
        if existing > 0:
            print("קורסים כבר קיימים")
            return
        
        courses = [
            Course(title="מבוא לקריפטו", description="למה ביטקוין ו-TON משנים את העולם", required_role="citizen", order_num=1),
            Course(title="CBDC והסכנות", description="למה מטבעות בנק מרכזי הם סיכון לחירות", required_role="citizen", order_num=2),
            Course(title="ביזור מול ריכוז", description="ההבדל בין מערכות מבוזרות לריכוזיות", required_role="entrepreneur", order_num=3),
        ]
        
        session.add_all(courses)
        await session.commit()
        print(f"✅ {len(courses)} קורסים נוספו")

asyncio.run(seed_courses())
