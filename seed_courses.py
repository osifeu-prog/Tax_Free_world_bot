import asyncio
from bot.database.session import async_session
from bot.database.models import Course
from sqlalchemy import text

async def seed():
    async with async_session() as session:
        # בדיקה אם כבר קיימים
        r = await session.execute(text("SELECT COUNT(*) FROM courses"))
        if r.scalar() > 0:
            print("✅ קורסים כבר קיימים, מדלג.")
            return

        courses = [
            Course(title="מבוא לקריפטו", description="למה ביטקוין ו‑TON משנים את העולם", required_role="citizen", order_num=1),
            Course(title="CBDC  מטבעות בנק מרכזי", description="ההבדל בין CBDC לקריפטו חופשי", required_role="citizen", order_num=2),
            Course(title="ביזור מול ריכוז", description="איך ביזור מונע שחיתות", required_role="citizen", order_num=3),
            Course(title="NFT וזהות דיגיטלית", description="איך NFT הופך לכרטיס ביקור דיגיטלי", required_role="entrepreneur", order_num=4),
            Course(title="DAO  ארגונים מבוזרים", description="לנהל קהילה עם חוזים חכמים", required_role="leader", order_num=5),
        ]
        session.add_all(courses)
        await session.commit()
        print(f"✅ {len(courses)} קורסים נוספו.")

asyncio.run(seed())
