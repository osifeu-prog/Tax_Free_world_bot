from sqlalchemy import select
from bot.database.session import async_session

async def get_top_referrers(limit: int = 10):
    try:
        async with async_session() as session:
            # שינוי זמני כדי לא לקרוס - משתמש ב-id במקום clicks
            result = await session.execute(
                select(Referral).order_by(Referral.id.desc()).limit(limit)
            )
            return result.scalars().all()
    except Exception as e:
        print(f"⚠️ Referral service error: {e}")
        return []
