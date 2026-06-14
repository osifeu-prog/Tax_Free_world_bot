from sqlalchemy import select
from bot.database.models import Referral  # נניח שהמודל קיים

async def get_top_referrers(limit: int = 10):
    # גרסה בטוחה - בודק אם השדה קיים
    try:
        async with async_session() as session:
            result = await session.execute(
                select(Referral).order_by(Referral.clicks.desc()).limit(limit)
            )
            return result.scalars().all()
    except AttributeError:
        # אם השדה clicks לא קיים - מחזיר ריק זמנית
        print("Warning: Referral.clicks does not exist yet")
        return []
