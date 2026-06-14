from sqlalchemy import select
from bot.database.session import async_session
from bot.database.models import Referral

async def get_top_referrers(limit: int = 10):
    try:
        async with async_session() as session:
            result = await session.execute(
                select(Referral).order_by(Referral.id.desc()).limit(limit)  # שינוי זמני כדי לא לקרוס
            )
            return result.scalars().all()
    except Exception as e:
        print(f"⚠️ Referral service error: {e}")
        return []
